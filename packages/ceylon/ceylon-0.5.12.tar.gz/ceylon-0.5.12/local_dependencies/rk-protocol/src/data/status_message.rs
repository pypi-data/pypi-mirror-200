use bincode::{config, Decode, Encode};

#[derive(Encode, Decode, PartialEq, Debug)]
pub enum StatusType {
    JOIN,
    LEAVE,
}

#[derive(Encode, Decode, PartialEq, Debug)]
pub struct StatusMessage {
    pub status_type: StatusType,
    pub meta: String,
}

impl StatusMessage {
    pub fn new(status_type: StatusType, meta: String) -> Self {
        Self {
            status_type,
            meta,
        }
    }

    pub fn new_join(meta: String) -> Self {
        Self::new(StatusType::JOIN, meta)
    }

    pub fn new_leave(meta: String) -> Self {
        Self::new(StatusType::LEAVE, meta)
    }

    pub fn encode(self) -> Vec<u8> {
        let config = config::standard();
        bincode::encode_to_vec(&self, config).unwrap()
    }

    pub fn decode(data: Vec<u8>) -> Self {
        let config = config::standard();
        let (message, _) = bincode::decode_from_slice(&data[..], config).unwrap();
        message
    }
}