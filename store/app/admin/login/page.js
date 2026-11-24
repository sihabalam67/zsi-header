'use client';
import { useActionState } from 'react';
import { login } from '../actions';

export default function Login() {
  const [state, action, pending] = useActionState(login, null);
  return (
    <section className="admin-login">
      <h1>Store admin</h1>
      <form action={action}>
        <label htmlFor="pw">Password</label>
        <input id="pw" name="password" type="password" autoComplete="current-password" required />
        <button className="cta" disabled={pending}>{pending ? 'Checking…' : 'Log in'}</button>
        {state?.error && <p className="error">{state.error}</p>}
      </form>
    </section>
  );
}
