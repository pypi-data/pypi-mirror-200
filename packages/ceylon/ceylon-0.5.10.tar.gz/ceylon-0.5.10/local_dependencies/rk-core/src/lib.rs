use std::sync::Arc;

use paris::{error, info};
use tokio;
use tokio::sync::mpsc::Sender;
use tokio::sync::Mutex;

pub use rk_protocol::data::{Message, MessageType};
pub use rk_protocol::data::data_message::{DataMessage, DataType};
pub use rk_protocol::data::status_message::{StatusMessage, StatusType};
use rk_protocol::transporter;

mod node;


const LOG_TARGET: &str = "core:: ";

#[derive(Debug, Clone)]
pub enum Mode {
    Leader,
    Follower,
    Dynamic,
}

#[derive(Debug, Clone)]
pub struct Config {
    pub mode: Mode,
}

impl Config {
    pub fn new(mode: Mode) -> Self {
        Self { mode }
    }

    pub fn leader() -> Self {
        Self::new(Mode::Leader)
    }

    pub fn follower() -> Self {
        Self::new(Mode::Follower)
    }

    pub fn dynamic() -> Self {
        Self::new(Mode::Dynamic)
    }
}

pub struct Core {
    pub(crate) config: Config,
    transporter: transporter::Transporter,
    node: Arc<Mutex<node::Node>>,
    node_id: String,
}

impl Core {
    pub fn new(config: Config) -> Self {
        let tr = transporter::Transporter::new();
        let peer_id = tr.local_peer_id.clone().to_string();
        Self {
            config,
            transporter: tr,
            node: Arc::new(Mutex::new(node::Node::new(peer_id.clone()))),
            node_id: peer_id.to_string(),
        }
    }

    pub async fn run(&mut self, _publisher: Sender<Message>) {
        info!("{LOG_TARGET}Core Started with mode: {:?}", self.config.mode);
        let (data_publisher, mut data_receiver) = tokio::sync::mpsc::channel::<Message>(1);
        let transport_publisher = self.transporter.sender();
        let node = self.node.clone();
        tokio::spawn(async move {
            while let Some(message) = data_receiver.recv().await {
                match _publisher.send(message.clone()).await {
                    Ok(_) => {}
                    Err(_) => error!("{LOG_TARGET}Error sending message to publisher"),
                };
                let mut node = node.lock().await;
                if message.message_type == MessageType::STATUS {
                    let status = StatusMessage::decode(message.clone().data);
                    if status.status_type == StatusType::JOIN && !node.has_child(message.peer_id.clone()) {
                        node.add_child(message.peer_id.clone());
                    }
                    // info!("{LOG_TARGET}Node Size: {}", node.len());
                    if node.len() > 0 {
                        match transport_publisher.send(
                            Message::new_data(
                                node.id.clone(),
                                DataMessage::new(DataType::SYSTEM, format!("Hello from {}", node.id).as_bytes().to_vec()).encode(),
                            )
                        ).await {
                            Ok(_) => {}
                            Err(_) => error!("{LOG_TARGET}Error sending Hello message to peer: {}", node.id),
                        };
                    }
                }
            }
        });
        self.transporter.run(data_publisher.clone()).await;
    }

    pub fn sender(&mut self) -> Sender<Message> {
        self.transporter.sender()
    }

    pub async fn node(&mut self) -> node::Node {
        self.node.clone().lock().await.clone()
    }

    pub fn get_node_id(&self) -> String {
        self.node_id.clone()
    }
}