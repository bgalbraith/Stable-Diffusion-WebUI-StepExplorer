let stepCursor = {txt: 0, img: 0};

function setupScroll(tab) {
    const buttons = gradioApp().querySelectorAll(`#${tab}2img_gallery.gradio-gallery * button.thumbnail-small`);
    if (buttons.length > 0) {
        const gallery = gradioApp().querySelector(`#${tab}2img_gallery.gradio-gallery`);
        gallery.onwheel = (event) => {
            event.preventDefault();
            const dir = Math.sign(event.deltaY);
            const nextStepCursor = Math.min(Math.max(0, (stepCursor[tab] - dir)), buttons.length - 1);
            if (stepCursor[tab] != nextStepCursor) {
                stepCursor[tab] = nextStepCursor;
                buttons[stepCursor[tab]].click();
            }            
        }      
    } 
}

onAfterUiUpdate(function() {
    setupScroll("txt");
    setupScroll("img");
    updateOnBackgroundChange();
});