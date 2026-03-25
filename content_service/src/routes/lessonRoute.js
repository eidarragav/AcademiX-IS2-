const express = require('express');
const router = express.Router();
const Lesson = require('../models/Lesson');

router.post('/', async (req, res) => {
    const lesson = await Lesson.create(req.body);
    res.json(lesson);
});

router.get('/', async (req, res) => {
    const lessons = await Lesson.find().populate('module_id');
    res.json(lessons);
});

router.get('/:id', async (req, res) => {
    const lesson = await Lesson.findById(req.params.id);
    res.json(lesson);
});

router.put('/:id', async (req, res) => {
    const lesson = await Lesson.findByIdAndUpdate(req.params.id, req.body, { new: true });
    res.json(lesson);
});

router.delete('/:id', async (req, res) => {
    await Lesson.findByIdAndDelete(req.params.id);
    res.json({ message: 'Eliminado' });
});

module.exports = router;