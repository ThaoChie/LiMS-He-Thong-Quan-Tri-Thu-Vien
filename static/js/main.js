/* LiMS - Main JavaScript */
document.addEventListener('DOMContentLoaded', function () {

    // --- Sidebar Toggle (Mobile) ---
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    const toggleBtn = document.querySelector('.btn-sidebar-toggle');

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function () {
            sidebar.classList.toggle('show');
            overlay.classList.toggle('show');
        });
    }
    if (overlay) {
        overlay.addEventListener('click', function () {
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
        });
    }

    // --- Active Nav Link ---
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar-nav .nav-link').forEach(function (link) {
        const href = link.getAttribute('href');
        if (href && href !== '/' && currentPath.startsWith(href)) {
            link.classList.add('active');
        } else if (href === '/' && currentPath === '/') {
            link.classList.add('active');
        }
    });

    // --- Auto-dismiss Alerts ---
    document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // --- Bootstrap Tooltips ---
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (el) {
        new bootstrap.Tooltip(el);
    });

    // --- Confirm Delete ---
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            if (!confirm(el.getAttribute('data-confirm') || 'Bạn có chắc chắn muốn xóa?')) {
                e.preventDefault();
            }
        });
    });

    // --- Star Rating UI ---
    document.querySelectorAll('.star-rating-input').forEach(function (container) {
        const stars = container.querySelectorAll('.star');
        const input = container.querySelector('input[type="hidden"]');
        stars.forEach(function (star) {
            star.addEventListener('click', function () {
                const val = parseInt(this.getAttribute('data-value'));
                input.value = val;
                stars.forEach(function (s, i) {
                    s.classList.toggle('filled', i < val);
                    s.innerHTML = i < val ? '<i class="bi bi-star-fill"></i>' : '<i class="bi bi-star"></i>';
                });
            });
            star.addEventListener('mouseenter', function () {
                const val = parseInt(this.getAttribute('data-value'));
                stars.forEach(function (s, i) {
                    s.style.color = i < val ? '#F59E0B' : '#CBD5E1';
                });
            });
        });
        container.addEventListener('mouseleave', function () {
            const current = parseInt(input.value) || 0;
            stars.forEach(function (s, i) {
                s.style.color = i < current ? '#F59E0B' : '#CBD5E1';
            });
        });
    });
});
