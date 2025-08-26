document.addEventListener('DOMContentLoaded', () => {
    const skillForm = document.getElementById('skill-form');
    const skillList = document.getElementById('skill-list');

    skillForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(skillForm);
        const skillData = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/api/skills', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(skillData),
            });

            if (response.ok) {
                const newSkill = await response.json();
                addSkillToList(newSkill);
                skillForm.reset();
            } else {
                console.error('Error adding skill:', response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    const addSkillToList = (skill) => {
        const skillItem = document.createElement('li');
        skillItem.textContent = `${skill.title} - ${skill.description} (Level: ${skill.level})`;
        skillList.appendChild(skillItem);
    };

    const loadSkills = async () => {
        try {
            const response = await fetch('/api/skills');
            const skills = await response.json();
            skills.forEach(addSkillToList);
        } catch (error) {
            console.error('Error loading skills:', error);
        }
    };

    loadSkills();
});