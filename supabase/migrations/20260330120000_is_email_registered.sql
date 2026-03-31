-- Allows the password-reset page to confirm the address exists before sending mail.
-- Run this migration in the Supabase SQL editor or via `supabase db push`.

create or replace function public.is_email_registered(candidate_email text)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
begin
  if candidate_email is null or length(trim(candidate_email)) = 0 then
    return false;
  end if;

  return exists (
    select 1
    from auth.users
    where lower(email) = lower(trim(candidate_email))
  );
end;
$$;

revoke all on function public.is_email_registered(text) from public;
grant execute on function public.is_email_registered(text) to anon, authenticated;

-- Refresh PostgREST so /rest/v1/rpc/is_email_registered is available immediately
notify pgrst, 'reload schema';
