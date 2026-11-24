// Licensed lifestyle photography (Pexels / Unsplash free licenses; credits in
// public/photos/credits.json). Product shots come from the supplier listing.
const photo = (file, alt) => ({ src: `/photos/${file}`, alt });

export const PHOTOS = {
  hero: photo('hero.jpg', 'An indoor cat crouched low, stalking a feather toy'),
  stalk: photo('stalk.jpg', 'A cat crouched low with its eyes locked on its target'),
  pounce: photo('pounce.jpg', 'A cat leaping and swatting at a toy'),
  feather: photo('feather.jpg', 'A cat batting at feathers'),
  rest: photo('rest.jpg', 'A cat curled up asleep after play'),
  window: photo('window.jpg', 'A cat sitting at a window, watching outside'),
  couch: photo('couch-play.jpg', 'Playing with a cat using a wand toy at home'),
  eyes: photo('eyes.jpg', 'Close-up of a cat’s eyes'),
};
