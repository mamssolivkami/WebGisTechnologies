document.addEventListener('DOMContentLoaded', function() {
    let addChildButton = document.getElementById('add-child');
    let totalForms = document.getElementById('id_child_set-TOTAL_FORMS');
    let childrenContainer = document.getElementById('children-container');
    let emptyFormTemplate = document.getElementById('empty-form-template').innerHTML;

    addChildButton.addEventListener('click', function() {
        let formIndex = parseInt(totalForms.value); 

        let newForm = document.createElement('div');
        newForm.innerHTML = emptyFormTemplate.replace(/__prefix__/g, formIndex); 

        let removeButton = newForm.querySelector('.remove-child');
        removeButton.addEventListener('click', function() {
            childrenContainer.removeChild(newForm);
            totalForms.value = parseInt(totalForms.value) - 1;
            updateFormIndexes(); 
        });

        childrenContainer.appendChild(newForm);

        totalForms.value = formIndex + 1;
    });

    function updateFormIndexes() {
        let forms = document.querySelectorAll('.child-form');
        forms.forEach((form, index) => {
            form.querySelectorAll('input, select, textarea').forEach(function(input) {
                let name = input.name.replace(/child_set-\d+/, `child_set-${index}`);
                let id = input.id.replace(/id_child_set-\d+/, `id_child_set-${index}`);
                input.name = name;
                input.id = id;
            });
        });
    }
});
