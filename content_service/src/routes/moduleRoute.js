const express = require('express');
const router = express.Router();
const Module = require('../models/Module');

router.post('/', async (req, res) => {
    const module = await Module.create(req.body);
    res.json(module);
});

router.get('/', async (req, res) => {
    const modules = await Module.find();
    res.json(modules);
});

router.get('/:id', async (req, res) => {
    const module = await Module.findById(req.params.id);
    res.json(module);
});

router.put('/:id', async (req, res) => {
    const module = await Module.findByIdAndUpdate(
        req.params.id,
        req.body,
        { new: true }
    );
    res.json(module);
});

router.delete('/:id', async (req, res) => {
    await Module.findByIdAndDelete(req.params.id);
    res.json({ message: 'Module eliminado' });
});

module.exports = router;