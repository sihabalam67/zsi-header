// Licensed lifestyle photography (Unsplash License: free commercial use; credits
// in public/photos/credits.json). Product shots come from the supplier listing.
const photo = (file, alt) => ({ src: `/photos/${file}`, alt });

export const PHOTOS = {
  hero: photo('hero.jpg', 'A kitten leaping at a feather toy in a sunlit living room'),
  stalk: photo('stalk.jpg', 'A tabby cat peeking over a table edge, eyes locked on its target'),
  pounce: photo('pounce.jpg', 'A kitten standing on its back legs, swatting at a toy'),
  feather: photo('feather.jpg', 'A fluffy cat on its back clutching a feather wand toy'),
  rest: photo('rest.jpg', 'A ginger and white cat asleep on a bed'),
  window: photo('window.jpg', 'A cat sitting at an open window, watching the trees outside'),
  couch: photo('couch-play.jpg', 'A tabby cat batting at a wand toy held by its owner'),
  eyes: photo('eyes.jpg', 'Close-up of a cat’s amber eyes'),
};
