const express = require('express');
const router = express.Router();
const Lesson = require('../models/Lesson');
require('dotenv').config();


function requireToken(req, res, next) {
    const token = req.headers["Authorization"];
    if (token !== `${process.env.SERVICES_TOKEN}`) {
        return res.status(403).json({ error: "No autorizado" });
    }
    next();
}

router.post('/', requireToken ,async (req, res) => {
    const lesson = await Lesson.create(req.body);
    res.json(lesson);
});

router.get('/',  requireToken , async (req, res) => {
    const lessons = await Lesson.find().populate('module_id');
    res.json(lessons);
});

router.get('/:id', requireToken , async (req, res) => {
    const lesson = await Lesson.findById(req.params.id);
    res.json(lesson);
});

router.put('/:id', requireToken , async (req, res) => {
    const lesson = await Lesson.findByIdAndUpdate(req.params.id, req.body, { new: true });
    res.json(lesson);
});

router.delete('/:id', requireToken , async (req, res) => {
    await Lesson.findByIdAndDelete(req.params.id);
    res.json({ message: 'Eliminado' });
});

module.exports = router;