import Link from 'next/link';
import { money, fromPrice } from '@/lib/product';

export default function ProductCard({ product }) {
  return (
    <Link href={`/products/${product.slug}`} className="pcard">
      <div className="pcard-img"><img src={product.images[0]} alt={product.name} width="600" height="600" loading="lazy" /></div>
      <div className="pcard-body">
        <small>{product.category}</small>
        <b>{product.name}</b>
        <span className="muted">{product.tagline}</span>
        <span className="price">{product.bundles.length > 1 ? 'From ' : ''}{money(fromPrice(product))}</span>
      </div>
    </Link>
  );
}
