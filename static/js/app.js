// MOBILE MENU

const mobileMenuBtn = document.querySelector(".menu-btn");
const mobileNavMenu = document.querySelector(".mobile-navs");
const mobileNavUl = document.querySelector(".mobile-navs nav ul");

// Toggles Mobile Menu
mobileMenuBtn.addEventListener("click", () => {
    mobileNavMenu.classList.toggle("open");
    if (mobileNavMenu.classList.contains("open")) {
        mobileMenuBtn.innerHTML = `<i class="fas fa-times"></i>`;
        setTimeout(() => mobileNavUl.classList.remove("not-visible"), 300);
        
    } else {
        mobileMenuBtn.innerHTML = `<i class="fas fa-align-left"></i>`;
        mobileNavUl.classList.add("not-visible");
    }
});


// ---------------------------------------------------------- ALL RECIPES

let categoriesHidden = false;

// Toggles Hidden Categories Cont
const toggleHiddenCat = () => {
    const toggleCategoriesBtn = document.querySelector(".toggle-categories-btn span");
    const allCategories = document.querySelectorAll(".categories-cont .category");

    console.log(allCategories.length)
    if (allCategories.length > 6 && !categoriesHidden) {
        allCategories.forEach((category, i) => {
            if (i > 5) {
                category.classList.add("hidden")
            }
        });
        toggleCategoriesBtn.innerText = "See All";
        categoriesHidden = true;
    } else {
        allCategories.forEach((category, i) => {
            if (i > 5) {
                category.classList.remove("hidden");
            }
        });
        toggleCategoriesBtn.innerText = "See Less";
        categoriesHidden = false;
    }

    // const hiddenCategories = document.querySelector(".categories-cont.hidden-categories-cont");

    // hiddenCategories.classList.toggle("hidden");
}


// 
const sortByDifficulty = recipes => {
    //
    const seperateByDifficulty = difficulty => difficulty.filter(d => d.dataset.category === difficulty)

    //
    const shuffleArray = array => {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    // 
    const setOrderArray = (recipes, arr1, arr2, arr3) => {
        if (recipes === "easy") {
            return [arr1, arr2, arr3];
        } else if (recipes === "medium") {
            return [arr2, arr3, arr1];
        } else if (recipes === "hard") {
            return [arr3, arr2, arr1];
        }
    }


    // declare array
    let easyRecipes = shuffleArray(seperateByDifficulty("easy"));
    let mediumRecipes = shuffleArray(seperateByDifficulty("medium"));
    let hardRecipes = shuffleArray(seperateByDifficulty("hard"));

    return setOrderArray(recipes, easyRecipes, mediumRecipes, hardRecipes);
}


// ---------------------------------------------------------- CREATE RECIPE
            
const dropFileForm = document.getElementById("dropFileForm");
const fileLabelText = document.getElementById("fileLabelText");
const uploadStatus = document.getElementById("uploadStatus");
const fileInput = document.getElementById("recipe_img");
let droppedFiles;


function overrideDefault(event) {
    event.preventDefault();
    event.stopPropagation();
}


function fileHover() {
    dropFileForm.classList.add("fileHover");
}


function fileHoverEnd() {
    dropFileForm.classList.remove("fileHover");
}


function addFiles(event) {
    droppedFiles = event.target.files || event.dataTransfer.files;
    showFiles(droppedFiles);
}


function showFiles(files) {
    if (files.length > 1) {
    fileLabelText.innerText = files.length + " files selected";
    } else {
    fileLabelText.innerText = files[0].name;
    }
}


function changeStatus(text) {
    uploadStatus.innerText = text;
}


// Deletes selected Ingredient Input
const removeIngredient = e => {
    if (e.target.parentElement.parentElement.classList.contains("ingredient-inputs")) {
        e.target.parentElement.parentElement.remove();
    }
    updateInputNames();
}


// Deletes selected Preparation Textarea
const removePreparationStep = e => {
    if (e.target.parentElement.parentElement.classList.contains("preparation-txtarea")) {
        e.target.parentElement.parentElement.remove();
    }
}


// Adds Three More Ingredient Inputs
const addThreeIngredientInputs = () => {
    const ingredientsCont = document.querySelector(".ingredients-cont");
    
    ingredientsCont.insertAdjacentHTML("beforeend", `
        <div class="ingredient-inputs flex-center">
            <div class="data-input amount">
                <input name="recipe_amount_0" type="number" min="0" required>
                <div class="input-underline"></div>
                <label for="recipe_amount">AMOUNT</label>
            </div>
            <div class="data-input unit">
                <input name="recipe_unit_0" min-length="1" maxlength="11" type="text" required>
                <div class="input-underline"></div>
                <label for="recipe_unit">UNIT</label>
            </div>
            <div class="data-input ingredient">
                <input name="recipe_ingredient_0" min-length="4" maxlength="25" type="text" required>
                <div class="input-underline"></div>
                <label for="recipe_ingredient">INGREDIENT</label>
            </div>
            <button onclick="removeIngredient(event)" class="remove-ingredient-btn">
                <i class="fas fa-times"></i>
            </button>
        </div>
        
        <div class="ingredient-inputs flex-center">
            <div class="data-input amount">
                <input name="recipe_amount_0" type="number" min="0" required>
                <div class="input-underline"></div>
                <label for="recipe_amount">AMOUNT</label>
            </div>
            <div class="data-input unit">
                <input name="recipe_unit_0" min-length="1" maxlength="11" type="text" required>
                <div class="input-underline"></div>
                <label for="recipe_unit">UNIT</label>
            </div>
            <div class="data-input ingredient">
                <input name="recipe_ingredient_0" min-length="4" maxlength="25" type="text" required>
                <div class="input-underline"></div>
                <label for="recipe_ingredient">INGREDIENT</label>
            </div>
            <button onclick="removeIngredient(event)" class="remove-ingredient-btn">
                <i class="fas fa-times"></i>
            </button>
        </div>
        
        <div class="ingredient-inputs flex-center">
            <div class="data-input amount">
                <input name="recipe_amount_0" type="number" min="0" required>
                <div class="input-underline"></div>
                <label for="recipe_amount">AMOUNT</label>
            </div>
            <div class="data-input unit">
                <input name="recipe_unit_0" min-length="1" maxlength="11" type="text" required>
                <div class="input-underline"></div>
                <label for="recipe_unit">UNIT</label>
            </div>
            <div class="data-input ingredient">
                <input name="recipe_ingredient_0" min-length="4" maxlength="25" type="text" required>
                <div class="input-underline"></div>
                <label for="recipe_ingredient">INGREDIENT</label>
            </div>
            <button onclick="removeIngredient(event)" class="remove-ingredient-btn">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `);
    updateInputNames();
}


// 
const updateInputNames = () => {
    const allInputConts = document.querySelectorAll(".ingredient-inputs");

    allInputConts.forEach((inputCont, index) => {
        let inputs = $($('.ingredient-inputs')[index]).find(':input');

        [...inputs].forEach((input) => {
            input.name = input.name.slice(0, -1) + index;
        });
    });
}


// Adds Two Preparation Steps (Textarea)
const addTwoPreparatrionTxtareas = () => {
    const preparationCont = document.querySelector(".preparation");
    
    preparationCont.insertAdjacentHTML("beforeend", `
        <div class="form-group preparation-txtarea">
            <button onclick="removePreparationStep(event)" class="delete-preparation-txtarea-btn">
                <i class="fas fa-times"></i>
            </button>
            <label class="about-label" for="about">PREPARATION STEP</label><br>
            <textarea id="about" name="about" class="about-txt-area" class="form-control" rows="3" maxlength="250"></textarea>
        </div>

        <div class="form-group preparation-txtarea">
            <button onclick="removePreparationStep(event)" class="delete-preparation-txtarea-btn">
                <i class="fas fa-times"></i>
            </button>
            <label class="about-label" for="about">PREPARATION STEP</label><br>
            <textarea id="about" name="about" class="about-txt-area" class="form-control" rows="3" maxlength="250"></textarea>
        </div>
    `);
}


// Changes Create Recipe Tab (by clicking) & Adds active class to Btns
const changeCreateRecipeTab = e => {
    const allCreateSections = document.querySelectorAll(".create-section");
    const allCreateTabsBtns = document.querySelectorAll(".create-steps-cont .create-step");
    
    allCreateTabsBtns.forEach(tabsBtn => {
        if (tabsBtn.classList.contains("active")) {
            tabsBtn.classList.remove("active");
        }
    });
    
    e.target.classList.add("active");
    
    allCreateSections.forEach(section => {
        if (!section.classList.contains("hidden")) {
        section.classList.add("hidden");
    }});
    
    allCreateSections.forEach(section => {
        if (section.classList.contains(e.target.dataset.tab)) {
            section.classList.remove("hidden");
        }
    });
}


// ---------------------------------------------------------- FILTER BY CATEGORY BUTTONS

// Gets category name of clicked btn
const getCategoryName = e => {
    let categoryName = e.target.dataset.category;

    filterByCategory(categoryName);
}


// Filters Recipe Cards by category name
const filterByCategory = categoryName => {
    const allRecipeCards = document.querySelectorAll(".recipe-card");

    //  [... allRecipeCards].filter(card => card.data === categoryName) 
    [... allRecipeCards].map(card =>  {
        if (card.classList.contains("hidden")) {
                card.classList.remove("hidden");
            }
        if (card.dataset.category !== categoryName) {
            card.classList.add("hidden");
        }
    }); 

}


const removeCategoryFilterUrl = currentUrl => {
    const allRecipeCards = document.querySelectorAll(".recipe-card");
    
    if (currentUrl.includes("/search")) {
        allRecipeCards.map(card => {
            if (card.classList.contains("hidden")) {
                card.classList.remove("hidden");
            }
        });
    }
}

// when clicking - cross / remove filter btn (click it - remove cross btn)

// header html - if admin - statt myProfile - modify categories
