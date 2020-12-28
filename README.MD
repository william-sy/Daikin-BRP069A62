# Daikin BPR069A62 Lan Adapter

## Intro

Welcome to the repository for the DAIKIN BRP-BRP069A62.
I moved all the 'old' files to the 'moved' folder. In favour of actually trying
to write a script that will do it all.

## Notes

currently the `main.py` helps you to find your daikin IP adrres based on mDNS.
It only finds 1 ip so if you have multiple heatpumps this might need some adaptation.

## Documentation
This will be in the `docs` directory

## For the time being:
You can find the old readme in /moved/readme.md

# Current status of project:

- Reading all data from the lan adapter needed to work with it:
- > DONE
- Sending new temperature:
- > DONE
- Sending new schedule ID (choose between schedules)
- > WIP
- Sending new schedule
- > WIP
- Display all data
- > TODO (All data is in database already)
- Create a TUI / Flask wrapper
- > TODO
- Documentation
- > Ongoing in the code itself, not formalized in the docs folder just yet
