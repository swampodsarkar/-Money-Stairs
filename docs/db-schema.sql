-- Postgres schema for eSports Tournament Platform (Supabase-friendly)
-- Safe to run on a fresh DB. Adjust auth references if using Supabase Auth.

create extension if not exists pgcrypto;

-- Enums
create type user_role as enum ('player','organizer','admin','super_admin');
create type tournament_type as enum ('1v1','2v2','squad','custom');
create type tournament_status as enum (
  'draft','pending_approval','approved','rejected',
  'registration_open','registration_closed','live','completed','canceled'
);
create type registration_status as enum ('pending','verified','canceled','refunded');
create type match_status as enum ('scheduled','live','completed','canceled');
create type transaction_type as enum ('deposit','withdrawal','entry_fee','prize','refund','adjustment');
create type transaction_status as enum ('pending','processing','succeeded','failed','canceled');
create type payout_status as enum ('pending','processing','paid','failed','canceled');
create type dispute_status as enum ('open','in_review','resolved','rejected');
create type participant_type as enum ('player','squad');
create type verification_method as enum ('otp','game_id','manual');
create type member_role as enum ('captain','member');
create type result_status as enum ('pending','verified','rejected');
create type approval_decision as enum ('approved','rejected');

-- Users (generic). If using Supabase, you may map to auth.users and keep this as profile table.
create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  phone text unique,
  display_name text not null,
  avatar_url text,
  country_code text,
  is_banned boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists user_roles (
  user_id uuid not null references users(id) on delete cascade,
  role user_role not null,
  primary key(user_id, role)
);

create table if not exists game_accounts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  game_name text not null,
  game_uid text not null,
  verified_at timestamptz,
  verification_method verification_method,
  created_at timestamptz not null default now(),
  unique(user_id, game_name),
  unique(game_name, game_uid)
);

-- Wallets & Transactions
create table if not exists wallets (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null unique references users(id) on delete cascade,
  currency text not null default 'USD',
  balance numeric(12,2) not null default 0 check (balance >= 0),
  locked_amount numeric(12,2) not null default 0 check (locked_amount >= 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists transactions (
  id uuid primary key default gen_random_uuid(),
  wallet_id uuid not null references wallets(id) on delete cascade,
  type transaction_type not null,
  status transaction_status not null default 'pending',
  amount numeric(12,2) not null check (amount >= 0),
  fee numeric(12,2) not null default 0 check (fee >= 0),
  currency text not null default 'USD',
  external_provider text,
  external_ref text,
  metadata jsonb not null default '{}',
  created_at timestamptz not null default now()
);
create index if not exists idx_transactions_wallet on transactions(wallet_id);
create index if not exists idx_transactions_created on transactions(created_at);

-- Tournaments
create table if not exists tournaments (
  id uuid primary key default gen_random_uuid(),
  organizer_id uuid not null references users(id) on delete cascade,
  title text not null,
  game_name text not null,
  type tournament_type not null,
  map text,
  match_time timestamptz,
  entry_fee numeric(12,2) not null default 0,
  currency text not null default 'USD',
  prize_pool numeric(12,2) not null default 0,
  min_participants int not null default 2 check (min_participants >= 1),
  max_participants int not null check (max_participants >= min_participants),
  status tournament_status not null default 'draft',
  otp_required boolean not null default false,
  game_id_required boolean not null default true,
  points_config jsonb not null default '{"kill_weight":1,"position_points":{"1":10,"2":6,"3":4}}',
  rules text,
  is_public boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_tournaments_status on tournaments(status);
create index if not exists idx_tournaments_game on tournaments(game_name);

create table if not exists tournament_approvals (
  id uuid primary key default gen_random_uuid(),
  tournament_id uuid not null unique references tournaments(id) on delete cascade,
  admin_id uuid not null references users(id) on delete set null,
  decision approval_decision not null,
  reason text,
  created_at timestamptz not null default now()
);

-- Squads & Registrations
create table if not exists squads (
  id uuid primary key default gen_random_uuid(),
  tournament_id uuid not null references tournaments(id) on delete cascade,
  name text not null,
  captain_id uuid not null references users(id) on delete restrict,
  created_at timestamptz not null default now(),
  unique(tournament_id, name)
);

create table if not exists squad_members (
  id uuid primary key default gen_random_uuid(),
  squad_id uuid not null references squads(id) on delete cascade,
  player_id uuid not null references users(id) on delete cascade,
  role member_role not null default 'member',
  joined_at timestamptz not null default now(),
  unique(squad_id, player_id)
);

create table if not exists registrations (
  id uuid primary key default gen_random_uuid(),
  tournament_id uuid not null references tournaments(id) on delete cascade,
  player_id uuid references users(id) on delete cascade,
  squad_id uuid references squads(id) on delete cascade,
  status registration_status not null default 'pending',
  game_uid text,
  otp_code text,
  verified_at timestamptz,
  created_at timestamptz not null default now(),
  check ((player_id is not null and squad_id is null) or (player_id is null and squad_id is not null))
);
create index if not exists idx_registrations_tournament on registrations(tournament_id);
create unique index if not exists uq_tournament_player on registrations(tournament_id, player_id) where player_id is not null;
create unique index if not exists uq_tournament_squad on registrations(tournament_id, squad_id) where squad_id is not null;

-- Matches & Results
create table if not exists matches (
  id uuid primary key default gen_random_uuid(),
  tournament_id uuid not null references tournaments(id) on delete cascade,
  round int not null default 1,
  map text,
  start_time timestamptz,
  status match_status not null default 'scheduled',
  server_info jsonb not null default '{}',
  created_at timestamptz not null default now()
);
create index if not exists idx_matches_tournament on matches(tournament_id);

create table if not exists match_participants (
  id uuid primary key default gen_random_uuid(),
  match_id uuid not null references matches(id) on delete cascade,
  participant_type participant_type not null,
  player_id uuid references users(id) on delete cascade,
  squad_id uuid references squads(id) on delete cascade,
  created_at timestamptz not null default now(),
  check ((participant_type = 'player' and player_id is not null and squad_id is null)
     or (participant_type = 'squad' and squad_id is not null and player_id is null))
);
create unique index if not exists uq_match_player on match_participants(match_id, player_id) where player_id is not null;
create unique index if not exists uq_match_squad on match_participants(match_id, squad_id) where squad_id is not null;

create table if not exists match_results (
  id uuid primary key default gen_random_uuid(),
  match_id uuid not null references matches(id) on delete cascade,
  player_id uuid references users(id) on delete cascade,
  squad_id uuid references squads(id) on delete cascade,
  kills int not null default 0 check (kills >= 0),
  points int not null default 0,
  rank int,
  proof_url text,
  submitted_by uuid not null references users(id) on delete set null,
  verified_by uuid references users(id) on delete set null,
  verified_at timestamptz,
  status result_status not null default 'pending',
  created_at timestamptz not null default now(),
  check ((player_id is not null and squad_id is null) or (player_id is null and squad_id is not null))
);
create index if not exists idx_results_match on match_results(match_id);
create index if not exists idx_results_status on match_results(status);

-- Leaderboard (materialized view example per tournament)
create materialized view if not exists leaderboard_entries as
select
  m.tournament_id,
  r.player_id,
  r.squad_id,
  sum(r.kills) as total_kills,
  sum(r.points) as total_points,
  count(distinct r.match_id) as matches_played
from match_results r
join matches m on m.id = r.match_id
where r.status = 'verified'
group by m.tournament_id, r.player_id, r.squad_id;

create index if not exists idx_leaderboard_tournament on leaderboard_entries(tournament_id);

-- Payouts
create table if not exists payouts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  tournament_id uuid references tournaments(id) on delete set null,
  amount numeric(12,2) not null check (amount > 0),
  currency text not null default 'USD',
  method text not null,
  account_ref text,
  status payout_status not null default 'pending',
  metadata jsonb not null default '{}',
  requested_at timestamptz not null default now(),
  processed_at timestamptz
);

-- Disputes
create table if not exists disputes (
  id uuid primary key default gen_random_uuid(),
  tournament_id uuid not null references tournaments(id) on delete cascade,
  match_id uuid references matches(id) on delete set null,
  raised_by uuid not null references users(id) on delete cascade,
  against_user_id uuid references users(id) on delete set null,
  reason text not null,
  details text,
  status dispute_status not null default 'open',
  resolution_notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_disputes_tournament on disputes(tournament_id);
create index if not exists idx_disputes_status on disputes(status);

-- Notifications & Push Subscriptions
create table if not exists notifications (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  type text not null,
  title text not null,
  body text not null,
  data jsonb not null default '{}',
  read_at timestamptz,
  created_at timestamptz not null default now()
);
create index if not exists idx_notifications_user on notifications(user_id);
create index if not exists idx_notifications_created on notifications(created_at);

create table if not exists push_subscriptions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  endpoint text not null unique,
  p256dh text not null,
  auth text not null,
  created_at timestamptz not null default now()
);

-- Chat
create table if not exists messages (
  id uuid primary key default gen_random_uuid(),
  tournament_id uuid not null references tournaments(id) on delete cascade,
  from_user_id uuid not null references users(id) on delete cascade,
  to_user_id uuid references users(id) on delete set null, -- null = channel message
  body text not null,
  created_at timestamptz not null default now(),
  read_at timestamptz
);
create index if not exists idx_messages_tournament on messages(tournament_id);

-- Fraud & Audit
create table if not exists fraud_flags (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  risk_score numeric(5,2) not null default 0 check (risk_score >= 0 and risk_score <= 100),
  reason text not null,
  details jsonb not null default '{}',
  created_at timestamptz not null default now(),
  resolved_at timestamptz,
  resolved_by uuid references users(id) on delete set null
);

create table if not exists audit_logs (
  id uuid primary key default gen_random_uuid(),
  actor_user_id uuid references users(id) on delete set null,
  action text not null,
  entity text not null,
  entity_id uuid,
  metadata jsonb not null default '{}',
  created_at timestamptz not null default now()
);

-- Utility trigger for updated_at
create or replace function set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end; $$;

create trigger trg_users_updated_at before update on users
for each row execute procedure set_updated_at();

create trigger trg_wallets_updated_at before update on wallets
for each row execute procedure set_updated_at();

create trigger trg_tournaments_updated_at before update on tournaments
for each row execute procedure set_updated_at();