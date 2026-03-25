const mongoose = require('mongoose');

const lessonSchema = new mongoose.Schema({
    title: {
        type: String,
        required: true
    },

    type: {
        type: String,
        enum: ['video', 'text', 'file'],
        required: true
    },

    module_id: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Module',
        required: true
    },

    content: {
        type: mongoose.Schema.Types.Mixed,
        required: true
    }

}, {
    timestamps: true
});

module.exports = mongoose.model('Lesson', lessonSchema);