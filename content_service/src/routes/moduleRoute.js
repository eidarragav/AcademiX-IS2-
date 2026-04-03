const express = require('express');
const router = express.Router();
const Module = require('../models/Module');

require('dotenv').config();


function requireToken(req, res, next) {
    const token = req.headers["Authorization"];
    if (token !== `${process.env.SERVICES_TOKEN}`) {
        return res.status(403).json({ error: "No autorizado" });
    }
    next();
}

router.post('/', requireToken, async (req, res) => {
    const module = await Module.create(req.body);
    res.json(module);
});

router.get('/', requireToken, async (req, res) => {
    const modules = await Module.find();
    res.json(modules);
});

const mongoose = require('mongoose');

router.get('/:id', requireToken, async (req, res) => {
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

router.put('/:id', requireToken, async (req, res) => {
    const module = await Module.findByIdAndUpdate(
        req.params.id,
        req.body,
        { new: true }
    );
    res.json(module);
});

router.delete('/:id', requireToken, async (req, res) => {
    await Module.findByIdAndDelete(req.params.id);
    res.json({ message: 'Module eliminado' });
});

module.exports = router;