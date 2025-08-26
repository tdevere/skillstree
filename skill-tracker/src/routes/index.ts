import { Router } from 'express';
import skillsRoutes from './skills';

const router = Router();

export default function setupRoutes(app) {
    app.use('/api/skills', skillsRoutes);
}