const mongoose = require('mongoose');

const moduleSchema = new mongoose.Schema({
    course_id:{
        type: Number,
        required: true
    },
    title: {
        type: String,
        required: true
    },
    description: String
}, {
    timestamps: true
});

module.exports = mongoose.model('Module', moduleSchema);