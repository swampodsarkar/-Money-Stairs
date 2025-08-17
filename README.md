# eSports Tournament Platform – MVP Docs

এই রিপোজিটরিতে আপনার টুর্নামেন্ট প্ল্যাটফর্মের MVP-এর জন্য প্রয়োজনীয় ডকুমেন্টেশন রাখা আছে: আর্কিটেকচার, ডাটাবেস স্কিমা, API স্পেক এবং ডেভেলপমেন্ট রোডম্যাপ।

## কী থাকবে (Scope)
- ইউজার: Player/Gamer, Organizer/Host, Admin/Super Admin
- ফিচার: রেজিস্ট্রেশন, এন্ট্রি ফি, যাচাই (OTP/গেম ID), টুর্নামেন্ট টাইপ (1v1/2v2/Squad/Custom), ল্যাডার/র‍্যাঙ্কিং, লাইভ স্কোরবোর্ড, পেমেন্ট (ডিপোজিট/উইথড্রল), নোটিফিকেশন, চ্যাট
- অ্যাডমিন: টুর্নামেন্ট এপ্রুভাল, ইউজার ম্যানেজমেন্ট, রিপোর্ট/লগস, কমপ্লেইন্ট/ডিসপিউট

## প্রস্তাবিত স্ট্যাক (MVP)
- Frontend: Next.js 14 (App Router), TypeScript, Tailwind CSS
- Backend: Supabase (Auth, Postgres, Realtime) + Edge Functions
  - বিকল্প: Node.js (NestJS/Express) সেবা কেবলমাত্র পেমেন্ট ও ওয়েবহুকের জন্য
- Realtime: Supabase Realtime (match_results এবং leaderboard সাবস্ক্রিপশন)
- Payments (MVP): PayPal (Card/Wallet)
  - পরবর্তীতে: Bank transfer, Mobile Wallet, Crypto (প্লাগ-ইন আর্কিটেকচার)
- Notifications: Web Push (VAPID) + Email
- Deployment: Vercel (FE), Supabase (DB/Realtime), Fly/Render (Webhook worker)

## লোকাল সেটআপ (গাইড)
1) Prerequisites: Node.js 20+, pnpm/yarn, Supabase CLI (ঐচ্ছিক)
2) Environment variables (.env.local):
```
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Payments (PayPal)
PAYPAL_CLIENT_ID=
PAYPAL_CLIENT_SECRET=
PAYPAL_WEBHOOK_ID=

# Web Push
WEB_PUSH_PUBLIC_KEY=
WEB_PUSH_PRIVATE_KEY=
```
3) ডাটাবেস স্কিমা: `docs/db-schema.sql` অনুযায়ী মাইগ্রেশন রান করুন (Supabase হলে `supabase db reset`/`db push`).
4) API কন্ট্রাক্ট: `docs/api-spec.yaml` দেখুন।
5) আর্কিটেকচার/ফ্লো: `docs/architecture.md` দেখুন।
6) রোডম্যাপ: `docs/mvp-roadmap.md` অনুসরণ করে ধাপে ধাপে ডেলিভার করুন।

## ফোল্ডার স্ট্রাকচার (প্রস্তাব)
```
/ (রুট)
├─ docs/
│  ├─ architecture.md
│  ├─ db-schema.sql
│  ├─ api-spec.yaml
│  └─ mvp-roadmap.md
├─ apps/
│  ├─ web/ (Next.js)
│  └─ worker/ (Webhook/Jobs)
└─ packages/
   ├─ ui/
   └─ sdk/ (API/Types shared)
```

## সিকিউরিটি/কমপ্লায়েন্স (সংক্ষেপ)
- KYC/AML (পেআউটের আগে): বেসিক ডকুমেন্টেশন + ম্যানুয়াল ভেরিফিকেশন
- Multi-account/Fraud Detection: ডিভাইস ফিঙ্গারপ্রিন্ট, IP/Proxy ফ্ল্যাগ, প্যাটার্ন অ্যানালাইসিস
- অডিট লগ: সব ক্রিটিকাল অ্যাকশন ট্র্যাক হবে

## স্ট্যাটাস
এই রিপোতে এখন মূলত ডকুমেন্টেশন রয়েছে। কোড স্ক্যাফোল্ড/ইমপ্লিমেন্টেশন `docs/mvp-roadmap.md` অনুযায়ী শুরু করুন।