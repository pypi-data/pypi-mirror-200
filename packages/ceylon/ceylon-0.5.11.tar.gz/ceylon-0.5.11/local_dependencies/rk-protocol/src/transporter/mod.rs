use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use std::time::Duration;

use futures::{FutureExt, StreamExt};
use futures::future::Either;
use libp2p::{gossipsub, identity, mdns, noise, PeerId, Swarm, tcp, Transport, yamux};
use libp2p::core::muxing::StreamMuxerBox;
use libp2p::core::transport::{Boxed, OrTransport};
use libp2p::swarm::{NetworkBehaviour, SwarmEvent};
use paris::{error, info, success};
use tokio::select;
use tokio::sync::mpsc::{Receiver, Sender};

use crate::data::{Message, MessageType};
use crate::data::status_message::StatusMessage;

const LOG_TARGET: &str = "transporter:: ";

pub struct Transporter {
    local_key: identity::Keypair,
    pub local_peer_id: PeerId,
    status_publisher: Sender<Message>,
    status_receiver: Receiver<Message>,
}

fn new_transport(keypair: identity::Keypair) -> Boxed<(PeerId, StreamMuxerBox)> {
    let mut config = libp2p::quic::Config::new(&keypair);
    config.handshake_timeout = Duration::from_secs(1);

    let quic_transport = libp2p::quic::async_std::Transport::new(config);
    let tcp_transport = tcp::async_io::Transport::new(tcp::Config::default())
        .upgrade(libp2p::core::upgrade::Version::V1Lazy)
        .authenticate(
            noise::NoiseConfig::xx(
                noise::Keypair::<noise::X25519Spec>::new()
                    .into_authentic(&keypair)
                    .unwrap(),
            )
                .into_authenticated(),
        )
        .multiplex(yamux::YamuxConfig::default());

    let transport = OrTransport::new(quic_transport, tcp_transport)
        .map(|either_output, _| match either_output {
            Either::Left((peer_id, muxer)) => (peer_id, StreamMuxerBox::new(muxer)),
            Either::Right((peer_id, muxer)) => (peer_id, StreamMuxerBox::new(muxer)),
        })
        .boxed();

    transport
}

#[derive(NetworkBehaviour)]
struct Behaviour {
    gossipsub: gossipsub::Behaviour,
    mdns: mdns::async_io::Behaviour,
}

impl Transporter {
    pub fn new() -> Self {
        let local_key = identity::Keypair::generate_ed25519();
        let local_peer_id = PeerId::from(local_key.public());
        info!("{LOG_TARGET} Peer initialized");
        info!("{LOG_TARGET} peer id: {:?}", local_peer_id.to_string());

        let (status_publisher, status_receiver) = tokio::sync::mpsc::channel(1);

        Self {
            local_key,
            local_peer_id,
            status_publisher,
            status_receiver,
        }
    }

    pub async fn run(&mut self, data_publisher: Sender<Message>) {
        let local_key = self.local_key.clone();
        let local_peer_id = self.local_peer_id.clone();

        let transport = new_transport(local_key.clone());

        let message_id_fn = |message: &gossipsub::Message| {
            let mut s = DefaultHasher::new();
            message.data.hash(&mut s);
            gossipsub::MessageId::from(s.finish().to_string())
        };

        // Set a custom gossipsub configuration
        let gossip_sub_config = gossipsub::ConfigBuilder::default()
            .heartbeat_interval(Duration::from_secs(10)) // This is set to aid debugging by not cluttering the log space
            .validation_mode(gossipsub::ValidationMode::Permissive) // This sets the kind of message validation. The default is Strict (enforce message signing)
            // .message_id_fn(message_id_fn) // content-address messages. No two messages of the same content will be propagated.
            .build()
            .expect("Valid config");

        let mut gossip_sub = gossipsub::Behaviour::new(
            gossipsub::MessageAuthenticity::Signed(local_key),
            gossip_sub_config,
        )
            .expect("Correct configuration");

        // Create a Gossipsub topic
        let topic = gossipsub::IdentTopic::new("test-net");

        // subscribes to our topic
        gossip_sub.subscribe(&topic).unwrap();

        // Create a Swarm to manage peers and events
        let mut swarm = {
            let config = mdns::Config {
                ..Default::default()
            };
            let mdns =
                mdns::async_io::Behaviour::new(config, local_peer_id).unwrap();
            let behaviour = Behaviour { gossipsub: gossip_sub, mdns };
            Swarm::with_async_std_executor(transport, behaviour, local_peer_id)
        };
        // Listen on all interfaces and whatever port the OS assigns
        swarm
            .listen_on("/ip4/0.0.0.0/tcp/0".parse().unwrap())
            .unwrap();

        // let mut status_receiver = self.data_receiver;
        loop {
            select! {
                status = self.status_receiver.recv().fuse()=>{
                    match status {
                    Some(msg) => {
                        // info!("Received message");
                        let topic_clone = topic.clone();
                        if msg.message_type == MessageType::STATUS {
                            let _status_message = StatusMessage::decode(msg.data);
                        } else if msg.message_type == MessageType::DATA {

                        // Step 3:::Send Message as a Event
                        // info!("{LOG_TARGET} Step 3:::Send Message as a Message {:?}",msg.data);
                            // let data_message = DataMessage::decode(msg.data);
                                if swarm.connected_peers().count()>0{
                                    match swarm.behaviour_mut().gossipsub.publish(topic_clone, msg.data){
                                    Ok(_) => {
                                }
                                Err(err) => {
                                    error!("{LOG_TARGET} Failed to publish message: {:?}", err);

                                    }                                                          };
                                }


                                                    }
                    }
                    e => {
                        error!("{LOG_TARGET}error: {:?}", e);
                    }
                    }
                }

                event = swarm.select_next_some() => match event {
                    SwarmEvent::Behaviour(BehaviourEvent::Mdns(mdns::Event::Discovered(list))) => {
                        for (peer_id, _multiaddr) in list {
                            match data_publisher.send(Message::new_status(peer_id.to_string(),StatusMessage::new_join(
                                format!("{LOG_TARGET}mDNS discovered a new peer: {peer_id}"),
                            ))).await{
                                Ok(_) => {
                                    success!("{LOG_TARGET}mDNS discovered a new peer sent: {peer_id}");
                                }
                                Err(err) => {
                                    error!("{LOG_TARGET}Failed to publish message: {:?}", err);
                                }
                            };
                            swarm.behaviour_mut().gossipsub.add_explicit_peer(&peer_id);
                        }
                    },
                    SwarmEvent::Behaviour(BehaviourEvent::Mdns(mdns::Event::Expired(list))) => {
                        for (peer_id, _multiaddr) in list {
                                match data_publisher.send(Message::new_status(peer_id.to_string(),StatusMessage::new_leave(
                                format!("{LOG_TARGET}mDNS expired a new peer: {peer_id}"),
                            ))).await{
                                Ok(_) => {
                                    success!("{LOG_TARGET}mDNS expired a new peer: {peer_id}");
                                }
                                Err(err) => {
                                    error!("{LOG_TARGET}Failed to publish message: {:?}", err);
                                }
                            };
                            swarm.behaviour_mut().gossipsub.remove_explicit_peer(&peer_id);
                        }
                    },
                    SwarmEvent::Behaviour(BehaviourEvent::Gossipsub(gossipsub::Event::Message {
                        propagation_source: peer_id,
                        message_id: _id,
                        message,
                    })) => {

                       // Step 4:::Rec Message
                       //  info!("{LOG_TARGET} Step 4:::Rec Message {:?}",message.data.clone());

                        let msg = Message::new(
                            MessageType::DATA,
                            peer_id.to_string(),
                           message.data.clone()
                        );
                        match data_publisher.send(msg).await{
                            Ok(_) => {
                            }
                            Err(err) => {
                                error!("Failed to publish message: {:?}", err);
                            }
                        }
                    },
                    _ => {}
                }
            }
        }
    }

    // pub async fn subscribe(&mut self) -> Receiver<Message> {
    //     self.status_receiver
    // }
    pub fn sender(&mut self) -> Sender<Message> {
        self.status_publisher.clone()
    }
}
