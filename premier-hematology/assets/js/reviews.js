(function () {
  document.querySelectorAll('.reviews-section[data-place-id]').forEach(function (section) {
    const placeId = section.dataset.placeId;
    const id = section.id || section.querySelector('[id]')?.closest('[id]')?.id || '';
    const carouselEl = section.querySelector('.reviews-carousel');
    const navEl = section.querySelector('.reviews-nav');
    const ratingEl = section.querySelector('.reviews-section__rating');

    if (!placeId || !carouselEl) return;

    fetch('/api/reviews?place_id=' + encodeURIComponent(placeId))
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (!data.reviews || !data.reviews.length) {
          section.style.display = 'none';
          return;
        }

        // Rating summary
        if (ratingEl && data.rating) {
          ratingEl.innerHTML =
            '<span class="reviews-stars">' + stars(data.rating) + '</span>' +
            '<span class="reviews-score">' + data.rating.toFixed(1) + '</span>' +
            '<span class="reviews-count">(' + data.total + ' reviews)</span>';
        }

        // Build cards
        carouselEl.innerHTML = data.reviews.map(function (r, i) {
          return '<div class="review-card' + (i === 0 ? ' review-card--active' : '') + '">' +
            '<div class="review-card__stars">' + stars(r.rating) + '</div>' +
            '<p class="review-card__text">' + escHtml(r.text) + '</p>' +
            '<div class="review-card__meta">' +
            '<img src="' + escHtml(r.avatar || '') + '" class="review-card__avatar" alt="" onerror="this.style.display=\'none\'">' +
            '<div><div class="review-card__author">' + escHtml(r.author) + '</div>' +
            '<div class="review-card__time">' + escHtml(r.time) + '</div></div>' +
            '</div></div>';
        }).join('');

        // Navigation dots
        if (navEl && data.reviews.length > 1) {
          navEl.innerHTML = data.reviews.map(function (_, i) {
            return '<button class="reviews-dot' + (i === 0 ? ' reviews-dot--active' : '') + '" data-idx="' + i + '" aria-label="Review ' + (i + 1) + '"></button>';
          }).join('');

          navEl.addEventListener('click', function (e) {
            const btn = e.target.closest('.reviews-dot');
            if (!btn) return;
            const idx = parseInt(btn.dataset.idx, 10);
            showCard(idx);
          });
        }

        // Auto-rotate every 6s
        let current = 0;
        const total = data.reviews.length;
        const timer = setInterval(function () {
          current = (current + 1) % total;
          showCard(current);
        }, 6000);
        section.addEventListener('mouseenter', function () { clearInterval(timer); });

        function showCard(idx) {
          current = idx;
          carouselEl.querySelectorAll('.review-card').forEach(function (c, i) {
            c.classList.toggle('review-card--active', i === idx);
          });
          if (navEl) {
            navEl.querySelectorAll('.reviews-dot').forEach(function (d, i) {
              d.classList.toggle('reviews-dot--active', i === idx);
            });
          }
        }
      })
      .catch(function () {
        section.style.display = 'none';
      });
  });

  function stars(rating) {
    const full = Math.round(rating);
    return '★'.repeat(full) + '☆'.repeat(5 - full);
  }

  function escHtml(str) {
    return String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
})();
