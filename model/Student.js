const mongoose = require('mongoose');
const Schema = mongoose.Schema;
//monggose

// Define collection and schema
let Student = new Schema({

  candidate_name: {
    type: String
  },
  candidate_email: {
    type: String
  },
  requirements:{
    type: Array
  },
  issueid:{
    type: String
  },
  similarity:{
    type: String
  },
  description:{
    type: String
  }
 
}, {
  collection: 'ciadata'
})

module.exports = mongoose.model('Student', Student)

