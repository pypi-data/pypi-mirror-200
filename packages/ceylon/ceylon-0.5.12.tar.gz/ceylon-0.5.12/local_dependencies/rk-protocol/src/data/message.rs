use crate::data::Message;

pub(crate) trait MessageUtils {
    fn convert_to_message(&self) -> Message;
    fn convert_from_message(message: Message) -> Self;
}