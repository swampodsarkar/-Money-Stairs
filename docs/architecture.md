### সিস্টেম আর্কিটেকচার (MVP)

- Frontend: Next.js 14 (TypeScript, Tailwind, App Router)
- Backend: Supabase (Auth, Postgres, Realtime) + Edge Functions
- Payments: PayPal (MVP) — Webhook worker service (Node.js)
- Notifications: Web Push (VAPID) + Email
- Realtime: Supabase Realtime (channels: `match_results`, `leaderboard`)

### হাই-লেভেল ডায়াগ্রাম (বর্ণনা)
- Client (Web) ↔ Supabase Auth
- Client (Web) ↔ Supabase Postgres (via RLS)
- Client (Web) ↔ Supabase Realtime (Live scoreboard, notifications)
- Worker (Webhook) ↔ PayPal APIs ↔ Postgres
- Admin Panel ↔ Same APIs + elevated scopes

### কী ডোমেইন
- Users/Roles: Player, Organizer, Admin, Super Admin
- Tournaments: Types (1v1, 2v2, Squad, Custom), Approval workflow
- Registrations: OTP/Game ID verification, Entry fee collection
- Matches & Results: Live updates, verification, disputes
- Wallet & Payments: Deposit/Withdraw, entry fee, prizes, payouts
- Ranking: Ladder system, configurable points
- Communications: In-app chat & notifications

### ডাটা ফ্লো (সংক্ষেপ)
1) Registration/Login
   - Email/Phone/Social → Supabase Auth → `users`, `user_roles`, `user_profiles`
2) Wallet Deposit
   - Client → create checkout (PayPal) → Webhook → `transactions` (succeeded) → `wallets.balance` update
3) Tournament Creation & Approval
   - Organizer → draft → submit → Admin review (`tournament_approvals`) → `tournaments.status=approved`
4) Player Registration
   - Balance ≥ entry_fee → hold/charge → `registrations` → verify (OTP/Game ID) → status=verified
5) Match & Live Score
   - Organizer schedules `matches` → players play → submit result/proof → moderator verifies → Realtime push to scoreboard
6) Payouts & Withdrawals
   - Prize allocation → `payouts` (processing) → method (PayPal/Bank/Wallet) → Webhook → status=paid

### র‍্যাঙ্কিং/ল্যাডার (উদাহরণ)
- পয়েন্ট = (kills × kill_weight) + position_points[rank]
- কনফিগ: `tournaments.points_config` (JSON)

### রিয়েলটাইম আপডেট
- Channels: `match_results` (per tournament), `leaderboard` (materialized view refresh trigger)
- ক্লায়েন্ট সাবস্ক্রাইব করে লাইভ স্কোর/স্ট্যাটস পায়

### সিকিউরিটি
- RLS (Row-Level Security) দিয়ে ডাটা আইসোলেশন
- Sensitive ops (ban/unban, approval) → `audit_logs`
- Rate limiting, device/IP fingerprints → `fraud_flags`

### স্কেলিং
- Read-heavy: use read replicas/materialized views for leaderboard
- Write bursts during match end: queue verification jobs
- File uploads (proof): S3/Supabase Storage, signed URLs

### মনিটরিং/অবজারভেবিলিটি
- App logs + DB logs → ড্যাশবোর্ড
- Alerting on payment webhook failures, RLS violations, high fraud risk