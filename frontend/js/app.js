document.addEventListener('DOMContentLoaded', () => {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const views = document.querySelectorAll('.view');
    const tabTriggers = document.querySelectorAll('.tab-trigger');

    function switchTab(targetId) {
        views.forEach(view => view.classList.add('hidden'));
        tabBtns.forEach(btn => btn.classList.remove('active'));

        const targetView = document.getElementById(targetId);
        if (targetView) {
            targetView.classList.remove('hidden');
        }

        const targetBtn = document.querySelector(`.tab-btn[data-target="${targetId}"]`);
        if (targetBtn) {
            targetBtn.classList.add('active');
        }
    }

    tabBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const targetId = e.target.getAttribute('data-target');
            switchTab(targetId);
        });
    });

    tabTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            const targetId = e.currentTarget.getAttribute('data-target');
            switchTab(targetId);
        });
    });
});