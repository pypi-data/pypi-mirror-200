use crate::data::status_message::StatusMessage;

pub mod status_message;
mod message;
pub mod data_message;

#[derive(Clone, Debug, PartialEq)]
pub enum MessageType {
    STATUS,
    DATA,
}


#[derive(Clone, Debug)]
pub struct Message {
    pub message_type: MessageType,
    pub peer_id: String,
    pub data: Vec<u8>,
}

impl Message {
    pub fn new(message_type: MessageType, peer_id: String, data: Vec<u8>) -> Self {
        Self {
            message_type,
            peer_id,
            data,
        }
    }

    pub fn new_status(peer_id: String, meta: StatusMessage) -> Self {
        Self::new(MessageType::STATUS, peer_id,  meta.encode())
    }

    pub fn new_data(peer_id: String, data: Vec<u8>) -> Self {
        Self::new(MessageType::DATA, peer_id, data)
    }
}