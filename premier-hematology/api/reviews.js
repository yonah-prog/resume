/**
 * /api/reviews?place_id=ChIJ...
 * Proxies Google Places Details API to avoid exposing the API key client-side.
 * Returns top 5 reviews (rating ≥ 4) plus overall rating + total count.
 *
 * Required env var: GOOGLE_PLACES_API_KEY
 */

module.exports = async function handler(req, res) {
  const { place_id } = req.query;
  if (!place_id) return res.status(400).json({ error: 'place_id required' });

  const key = process.env.GOOGLE_PLACES_API_KEY;
  if (!key) return res.status(500).json({ error: 'Google Places API key not configured' });

  const url = `https://maps.googleapis.com/maps/api/place/details/json` +
    `?place_id=${encodeURIComponent(place_id)}` +
    `&fields=rating,user_ratings_total,reviews` +
    `&reviews_sort=newest` +
    `&key=${key}`;

  try {
    const upstream = await fetch(url);
    const json = await upstream.json();

    if (json.status !== 'OK') {
      return res.status(502).json({ error: json.status, message: json.error_message });
    }

    const { rating, user_ratings_total, reviews = [] } = json.result;

    // Filter to 4-5 star reviews for display
    const filtered = reviews
      .filter(r => r.rating >= 4)
      .slice(0, 5)
      .map(r => ({
        author: r.author_name,
        avatar: r.profile_photo_url,
        rating: r.rating,
        text: r.text,
        time: r.relative_time_description,
      }));

    res.setHeader('Cache-Control', 's-maxage=86400, stale-while-revalidate');
    return res.status(200).json({ rating, total: user_ratings_total, reviews: filtered });
  } catch (err) {
    console.error('Places API error:', err);
    return res.status(500).json({ error: 'Failed to fetch reviews' });
  }
};
