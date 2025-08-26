import { Router } from 'express';
import SkillsController from '../controllers/skillsController';

const router = Router();
const skillsController = new SkillsController();

router.post('/skills', skillsController.createSkill.bind(skillsController));
router.get('/skills', skillsController.getSkills.bind(skillsController));
router.get('/skills/:id', skillsController.getSkillById.bind(skillsController));
router.put('/skills/:id', skillsController.updateSkill.bind(skillsController));
router.delete('/skills/:id', skillsController.deleteSkill.bind(skillsController));

export default router;