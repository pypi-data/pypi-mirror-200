use std::collections::HashMap;
use std::sync::Arc;

use paris::error;
use pyo3::prelude::*;
use pyo3::types::{PyAny, PyBytes, PyString};
use tokio::sync::{mpsc, Mutex, RwLock};
use tokio::sync::mpsc::channel;

use rk_core::{DataMessage, DataType, Message, MessageType};

use crate::executors::execute_event_handler;

mod executors;

const LOG_TARGET: &str = "pythonlib:: ";

pub struct Event {
    pub sender: String,
    pub topic: String,
    pub message: Vec<u8>,
}

#[pyclass]
struct PubSub {
    subscribers: Arc<RwLock<HashMap<String, Vec<PyObject>>>>,
    publish_sender: Arc<Mutex<mpsc::Sender<Event>>>,
    publish_receiver: Arc<Mutex<mpsc::Receiver<Event>>>,
    core: Arc<Mutex<rk_core::Core>>,
    id: String,
}

#[pymethods]
impl PubSub {
    #[new]
    fn new() -> Self {
        let (publish_sender, publish_receiver) = mpsc::channel::<Event>(1);

        let subscribers = Arc::new(RwLock::new(HashMap::<String, Vec<PyObject>>::new()));
        // let cloned_subscribers = Arc::clone(&subscribers);

        let conf = rk_core::Config::dynamic();
        // Pass the PubSub instance to the Core struct (update your Core implementation to accept it)
        let core = rk_core::Core::new(conf);
        let id = core.get_node_id().clone();


        PubSub {
            subscribers,
            publish_sender: Arc::new(Mutex::new(publish_sender)),
            publish_receiver: Arc::new(Mutex::new(publish_receiver)),
            core: Arc::new(Mutex::new(core)),
            id: id.to_string(),
        }
    }

    fn subscribe<'a>(&'a self, py: Python<'a>, topic: String, callback: PyObject) -> PyResult<&'a PyAny> {
        let subscribers = self.subscribers.clone();
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let mut subscribers = subscribers.write().await;
            subscribers
                .entry(topic)
                .or_insert_with(Vec::new)
                .push(callback);
            Ok(())
        })
    }

    fn publish<'a>(&'a self, _py: Python<'a>, topic: String, data: Vec<u8>) -> PyResult<()> {
        let publish_sender = self.publish_sender.clone();
        let runtime = pyo3_asyncio::tokio::get_runtime();
        let publisher_id = self.id.clone();
        runtime.spawn(async move {
            let publish_sender = publish_sender.lock().await;

            let message = DataMessage {
                status_type: DataType::NODE,
                meta: data,
            };
            // Step 1:::Send Message as a Event
            // info!("{LOG_TARGET} Step 1:::Send Message as a Event");
            match publish_sender.send(Event {
                sender: publisher_id,
                topic: topic.clone(),
                message: message.encode(),
            }).await {
                Ok(_) => {}
                Err(e) => {
                    error!("{LOG_TARGET}Error sending message to subscribers inside publish {e}");
                }
            }
        });

        Ok(())
    }

    fn start<'a>(&'a self, py: Python<'a>) -> PyResult<&'a PyAny> {
        let core = self.core.clone();
        let publish_sender = self.publish_sender.clone();
        let publish_receiver = self.publish_receiver.clone();

        let publisher_id = self.id.clone();
        let cloned_subscribers = self.subscribers.clone();
        pyo3_asyncio::tokio::future_into_py(py, async move {
            // ... The rest of the start_core implementation
            let (tx, mut rx) = channel::<Message>(1);
            let runtime = pyo3_asyncio::tokio::get_runtime();

            let mut core = core.lock().await;
            let sender = core.sender();
            runtime.spawn(async move {
                let mut publisher_receiver = publish_receiver.lock().await;
                while let Some(event) = publisher_receiver.recv().await {
                    let sender_id = event.sender;
                    let topic = event.topic;
                    let message = event.message.clone();
                    if sender_id == publisher_id.clone() {
                        // Step 2:::Send Message as a Event
                        // info!("{LOG_TARGET} Step 2:::Send Message as a Message {message:?}");
                        match sender.send(Message {
                            peer_id: sender_id,
                            message_type: MessageType::DATA,
                            data: message,
                        }).await {
                            Ok(_) => {}
                            Err(e) => {
                                error!("{LOG_TARGET}Error sending message to subscribers inside publish {e}");
                            }
                        };
                        continue;
                    } else {
                        let subscribers = cloned_subscribers.read().await;
                        Python::with_gil(|py| {
                            let meta = DataMessage::decode(message);
                            let py_message = PyBytes::new(py, &meta.meta);
                            if let Some(callbacks) = subscribers.get(&topic) {
                                for callback in callbacks {
                                    let ex = execute_event_handler(callback.clone_ref(py), py_message.to_object(py));
                                    runtime.spawn(async move {
                                        let ex = ex;
                                        match ex.await {
                                            Ok(_) => {}
                                            Err(e) => {
                                                error!("{LOG_TARGET}Error sending message to subscribers inside publish {e}");
                                            }
                                        }
                                    });
                                }
                            }
                        });
                    }
                }
            });

            runtime.spawn(async move {
                while let Some(message) = rx.recv().await {

                    // Step 4:::Rec Message
                    // info!("{LOG_TARGET} Step 5:::Rec Message {:?}",message.data.clone());

                    let publish_sender = publish_sender.lock().await;
                    let data_message = DataMessage::decode(message.data.clone());
                    let publisher_id = message.peer_id.clone();
                    match publish_sender.send(Event {
                        sender: publisher_id,
                        topic: "agent_topic".to_string(),
                        message: data_message.encode(),
                    }).await {
                        Ok(_) => {}
                        Err(e) => {
                            error!("{LOG_TARGET} Error sending message to subscribers inside publish {e}");
                        }
                    }
                }
            });

            core.run(tx.clone()).await;
            Ok(Python::with_gil(|py| Python::None(py)))
        })
    }


    pub fn get_node_id<'a>(&'a self, py: Python<'a>) -> PyResult<&'a PyString> {
        let id = self.id.clone();
        Ok(PyString::new(py, id.as_str()))
    }
}


/// Formats the sum of two numbers as string.
// #[pyfunction]
// fn start_core(py: Python) -> PyResult<&PyAny> {}
#[pyfunction]
fn python_string_to_vec_u8(_py: Python, py_data: &PyBytes) -> PyResult<Vec<u8>> {
    let vec_u8 = py_data.as_bytes().to_vec();
    Ok(vec_u8)
}

/// A Python module implemented in Rust.Z
#[pymodule]
fn ceylon(_py: Python, m: &PyModule) -> PyResult<()> {
    pyo3_log::init();
    m.add_class::<PubSub>()?;
    m.add_function(wrap_pyfunction!(python_string_to_vec_u8, m)?)?;
    Ok(())
}