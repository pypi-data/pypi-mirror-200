use bincode::{config, Decode, Encode};

#[derive(Encode, Decode, PartialEq, Debug, Clone)]
pub enum DataType {
    SYSTEM,
    NODE,
}

#[derive(Encode, Decode, PartialEq, Debug, Clone)]
pub struct DataMessage {
    pub status_type: DataType,
    pub meta: Vec<u8>,
}

impl DataMessage {
    pub fn new(status_type: DataType, meta: Vec<u8>) -> Self {
        Self {
            status_type,
            meta,
        }
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