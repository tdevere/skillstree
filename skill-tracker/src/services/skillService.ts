export class SkillService {
    private skills: Array<{ title: string; description: string; level: number }> = [];

    public addSkill(title: string, description: string, level: number): void {
        const newSkill = { title, description, level };
        this.skills.push(newSkill);
    }

    public getSkills(): Array<{ title: string; description: string; level: number }> {
        return this.skills;
    }

    public updateSkill(index: number, title: string, description: string, level: number): void {
        if (index >= 0 && index < this.skills.length) {
            this.skills[index] = { title, description, level };
        }
    }

    public deleteSkill(index: number): void {
        if (index >= 0 && index < this.skills.length) {
            this.skills.splice(index, 1);
        }
    }
}