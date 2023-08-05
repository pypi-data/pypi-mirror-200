"""
Seed ID: ${seed_id}
Created At: ${created_at}
"""

${imports if imports else ""}

seed_id = "${seed_id}"
% if previous_seed_id:
previous_seed_id = "${previous_seed_id}"
% else:
previous_seed_id = None
% endif

async def seed():
    pass