---
captured: 2026-08-08T00:56:37+00:00
session: 89ffe221-5003-4154-b532-401af1f1b43e
cwd: /Users/chidionyema/Documents/code/prospector
chars: 8401
source: founder prompt, verbatim (founder-doc-capture.py)
---

Verified both blockers. R3 is a false alarm — the spec's hypothesis was wrong. R1 has a partial answer.                                                                         
                                                                                                                                                                                 
 R3 (menu push unverified): FALSE                                                                                                                                                
 - Production call site: gateway/platforms/telegram.py:2366 (startup, for Default / AllPrivateChats / AllGroupChats scopes) and :6515 (forum lazy-registration on first message) 
 - The spec's grep missed gateway/platforms/telegram.py (it grepped only commands.py and tests). The function telegram_bot_commands() at commands.py:594 is just the data        
   builder — the actual push lives in the gateway adapter.                                                                                                                       
 - The hard cap is MAX_COMMANDS_PER_SCOPE = 30, not 12. The "12" comes from operator_shell.menu_profile: operator in config.yaml:433,568 filtering to OPERATOR_TELEGRAM_MENU (12 
   names) in gateway/operator_shell/menu.py:14-28.                                                                                                                               
 - Caveat: the push is startup-only. A menu-priority change takes effect on the next gateway restart, not in-session. The 31 Jul fix would have worked — after a restart.        
                                                                                                                                                                                 
 R1 (config re-read): YES, with one qualifier                                                                                                                                    
 - load_config() uses an mtime+size cache (hermes_cli/config.py:5295 docblock: "cached on the config file's (mtime_ns, size). Returns a deepcopy of the cached value when        
   unchanged... save_config() + migrate_config() write via atomic_yaml_write which produces a fresh inode, so stat() sees a new mtime_ns and the next load repopulates           
   automatically — no explicit invalidation hook."). So the gateway picks up a config.yaml change on its next load_config() call.                                                
 - Caveat: that re-read is per-process. A long-lived model instance (e.g. one already constructed in memory) keeps the old provider until the next instantiation. For the Brains 
   panel this means: writing a new role model is reflected on the next dispatch for that role, not on the in-flight one. The panel must say so, or it's a lie with a tick next   
   to it.                                                                                                                                                                        
                                                                                                                                                                                 
 Two facts the spec got right                                                                                                                                                    
 - agent_model is registered (commands.py:152, gateway_only=True, aliases agentmodel, brain) but absent from OPERATOR_TELEGRAM_MENU (which is panel, projects, dashboard,        
   status, inbox, brief, cron, busy, notify, revert, missions, help). Typeable, never advertised — exactly as the spec says.                                                     
 - The 13 roles under auxiliary: in config.yaml:119-212 are all provider: auto / model: ''. Confirmed, with the exact role list the spec names. Zero UI surfaces for any of      
   them.                                                                                                                                                                         
                                                                                                                                                                                 
 Implication for the plan                                                                                                                                                        
                                                                                                                                                                                 
 R3 is not a blocker — the menu push is wired and works on restart. R1 needs a runtime test (change one role, dispatch, observe the actual model used) before P2 ships, but it's 
 not blocking P0/P1 either.                                                                                                                                                      
                                                                                                                                                                                 
 The "1 tap to your original question" target is achievable today with a one-line config change: add agent_model to OPERATOR_TELEGRAM_MENU. That is P0. The persistent reply     
 keyboard (P1) is the right next move and unblocks the Brains panel naturally because it gives the surface a place to render the role list.                                      
                                                                                                                                                                                 
 Recommendation: ship P0 + P1 as one coordinated change, not two.                                                                                                                
                                                                                                                                                                                 
 - P0 part: add agent_model to OPERATOR_TELEGRAM_MENU and make /agent_model print current state before the picker (state-before-verb, principle 3). Pure config + a one-line     
   handler edit; takes effect on the next gateway restart.                                                                                                                       
 - P1 part: persistent ReplyKeyboardMarkup door with the five buttons the spec names (🎛 Now, 🤖 Brains, ⚙️ Control, 📥 Inbox, ❓ All). The / menu stays as the fallback for the  
   30-command overflow.                                                                                                                                                          
 - P2 (Brains panel) then renders into the 🤖 Brains button slot and is the thing the user actually asked for.                                                                   
 - P3 reachability gate lands alongside P2 so the 12-vs-30 drift can't return.                                                                                                   
                                                                                                                                                                                 
 Two things to confirm before I start coding:                                                                                                                                    
 1. The "Operator Telegram menu" file at gateway/operator_shell/menu.py is the right knob for P0. Are you OK with restarting the gateway to land P0, or do you want P0 to be a   
    no-restart change (which would mean not touching the visible Telegram menu this round and only fixing the /agent_model handler's state-before-verb behaviour)?               
 2. The R1 runtime test (change role → dispatch → observe) — do you want me to do it as part of P2, or earlier, before P1?                                                       
                                                                                                                                                                                 
 Say the word and I'll start. I'd also like to append a 2026-08-08 row to the spec's §5 ledger recording that R3 was re-verified false, so this can't drift again.   , recall we eed to nake the ui and u eponentiy better
