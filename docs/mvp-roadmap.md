### MVP Development Flow (৮–১০ সপ্তাহ)

#### ধাপ 1: User Registration & Login (সপ্তাহ ১)
- Email/Phone/Social login (Supabase Auth)
- Profile: নাম, এভাটার, র‍্যাংক (ডামি), গেম ID লিংক
- Acceptance: Signup/Login কাজ করে, প্রোফাইল আপডেটযোগ্য, Ban ইউজার লগইন করতে পারে না

#### ধাপ 2: Wallet Integration & Payment Setup (সপ্তাহ ২)
- Wallet টেবিল, ব্যালান্স দেখানো
- PayPal deposit checkout + webhook (success → balance add)
- Transactions history
- Acceptance: ডিপোজিট করলে ব্যালান্স আপডেট, ট্রানজেকশন দেখা যায়

#### ধাপ 3: Tournament Creation (Host) (সপ্তাহ ৩)
- Organizer: Create/Draft, Submit for approval
- Admin: Approve/Reject + Audit logs
- Acceptance: Approved হলে `registration_open`

#### ধাপ 4: Tournament Registration (Player) (সপ্তাহ ৪)
- Entry fee deduction/hold, Registration record
- OTP/Game ID verification flow
- Acceptance: Verified হলে অংশগ্রহণকারী তালিকায় দেখা যায়

#### ধাপ 5: Matches & Live Score (সপ্তাহ ৫–৬)
- Match schedule/generate
- Result submission + proof upload
- Moderator verify →实时 scoreboard update
- Acceptance: Leaderboard realtime আপডেট হয়

#### ধাপ 6: Earnings Calculation & Withdrawal (সপ্তাহ ৭)
- Prize allocation (configurable points → payouts)
- Withdraw request (PayPal), webhook update → paid
- Acceptance: সফল উইথড্রল ট্র্যাক হয়

#### ধাপ 7: Admin Dashboard & Controls (সপ্তাহ ৮)
- Users list/ban-unban, Tournaments pending/approve/reject
- Reports (Daily/Weekly basic KPIs)
- Acceptance: অ্যাডমিন সকল কোর অপারেশন করতে পারে

### Plus Features (পরবর্তী)
- Chat threading, mentions, moderation tools
- Fraud detection automation (device id, IP risk)
- Mobile Wallet/Bank/Crypto integrations
- Advanced analytics, exportable reports

### ডেলিভারেবলস
- Docs: আর্কিটেকচার, DB, API (এই রিপো)
- Infra: Supabase project, PayPal sandbox, Web push keys
- App: Web (Next.js), Worker (Webhook)

### Success Criteria
- 100 জন কনকারেন্ট ইউজার, ১টি লাইভ টুর্নামেন্টে রিয়েলটাইম স্কোরবোর্ড
- Payment success/failure webhook 99%+ প্রসেসিং নির্ভুলতা
- Dispute resolution SLA ≤ 24h