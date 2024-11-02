export default class ChildFormManager {
    constructor() {
        this.addChildButton = document.getElementById('add-child');
        this.totalForms = document.getElementById('id_child_set-TOTAL_FORMS');
        this.childrenContainer = document.getElementById('children-container');
        this.emptyFormTemplate = document.getElementById('empty-form-template').innerHTML;

        this.init();
    }

    init() {
        this.addChildButton.addEventListener('click', () => this.addChildForm());
    }

    addChildForm() {
        const formIndex = parseInt(this.totalForms.value);
        const newForm = document.createElement('div');
        newForm.innerHTML = this.emptyFormTemplate.replace(/__prefix__/g, formIndex);

        const removeButton = newForm.querySelector('.remove-child');
        removeButton.addEventListener('click', () => {
            this.childrenContainer.removeChild(newForm);
            this.totalForms.value = parseInt(this.totalForms.value) - 1;
            this.updateFormIndexes();
        });

        this.childrenContainer.appendChild(newForm);
        this.totalForms.value = formIndex + 1;
    }

    updateFormIndexes() {
        const forms = this.childrenContainer.querySelectorAll('.child-form');
        forms.forEach((form, index) => {
            form.querySelectorAll('input, select, textarea').forEach((input) => {
                input.name = input.name.replace(/child_set-\d+/, `child_set-${index}`);
                input.id = input.id.replace(/id_child_set-\d+/, `id_child_set-${index}`);
            });
        });
    }
}
