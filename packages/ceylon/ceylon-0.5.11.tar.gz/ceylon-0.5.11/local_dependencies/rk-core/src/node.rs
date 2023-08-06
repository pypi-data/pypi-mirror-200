use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct Node {
    pub id: String,
    pub children: HashMap<String, Node>,
}

impl Node {
    pub fn new(id: String) -> Self {
        Self {
            id,
            children: HashMap::new(),
        }
    }

    pub fn add_child(&mut self, id: String) {
        self.children.insert(id.clone(), Node::new(id.clone()));
    }

    pub fn has_child(&self, id: String) -> bool {
        self.children.contains_key(&id)
    }

    pub fn len(&self) -> usize {
        self.children.len()
    }
}