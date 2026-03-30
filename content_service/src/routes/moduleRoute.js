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

const mongoose = require('mongoose');

router.get('/:id', async (req, res) => {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
        return res.status(400).json({ message: 'Invalid ID format' });
    }

    try {
        const module = await Module.findById(id);

        if (!module) {
            return res.status(404).json({ message: 'Module not found' });
        }

        res.json(module);

    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
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