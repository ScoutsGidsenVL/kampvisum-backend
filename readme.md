
# **Welcome to the kampvisum app**  

## **SETUP**  

Most of the time, a simple `django_manage.py migrate` should be sufficient to create and run migrations.  
If this should fail, there is a script that specifically makes and runs migrations for every app:  
`scripts/migrations.sh`

For setup through other means, the following commands should be run, in the following order and after `migrate`:  
- runfixtures
- setupcampyears

The category, sub-category, check and deadline structure for a camp year is no longer seeded from fixtures. It lives in the database, seeded historically for existing camp years, and new camp years are created by cloning the previous one (see below).  

## **SETTINGS**  

   - `ACTIVITY_EPOCH`  
     Default 0 for limitless. A setting that determines (in number of years) when a member is considered inactive after the last active function.  
     This is used for instance in filtering member searches on the groupadmin.  
   - `CAMP_REGISTRATION_EPOCH`  
     A setting that determines when in the course of the year a newly registered camp should be considered to be part of the next camp year, instead of the current one.  
   - `RESPONSIBILITY_EPOCH`
     A setting that determines when the camp responsibles have to take extra action if a responsible person changes.
   - `IS_ACCEPTANCE`  
     If True and DEBUG=True, then emails will be sent to the debug address.  
   - `DEBUG`  
   - `LOGGING_LEVEL`  
     Determines the level of logging for all apps.  
   - `LOGGING_LEVEL_ROOT`  
     Determines the level of logging for django's own logging.  
   - `DEFAULT_FILE_STORAGE`  
   - `DEFAULT_FILE_STORAGE=scouts_auth.inuits.files.aws.S3StorageService`  
   - `USE_S3_STORAGE`  
   - If set to True, then the storage backend used will be `scouts_auth.inuits.files.aws.S3StorageService`  
   - `USE_SEND_IN_BLUE`  
     If set to True, then emails will be sent through SendInBlue

## **EDITING i18N (FRONTEND)**  

In frontend repo: `/src/locales/nl.json`  
- Copy the text in the frontend
- Search for it in the locale file
- Replace with the desired text
- GITHUB: If editing through the github interface: click 'commit changes', otherwise:
- GIT:
  * `git add src/locales/nl.json`
  * `git commit -m "a sensible commit message that accurately reflects the changes"`
  * `git push origin master`

## **EDITING CATEGORIES, SUB-CATEGORIES AND CHECKS**

Categories, sub-categories and checks are no longer defined in fixtures. Historical camp years (2022 up to and including 2026) were seeded once and now live only in the database. A new camp year is created by cloning the previous one, not by editing JSON.

Check types are still defined in `src/apps/visums/fixtures/check_types.json` and change rarely, since a new check type requires matching frontend support:
   - **SimpleCheck**  
     A check that can be checked, unchecked or set as not applicable  
   - **DateCheck**  
     A check that contains a date  
     Currently unused.  
   - **DurationCheck**  
     A check that contains a start and end date  
   - **LocationCheck**  
     A check that contains one or more geo-coordinates  
   - **CampLocationCheck**  
     A check that contains one or more geo-coordinates and contact details  
   - **ParticipantCheck**  
		 A check that selects members and non-members  
   - **ParticipantMemberCheck**  
     A check that selects members  
   - **ParticipantCookCheck**  
     A check that selects cooks
   - **ParticipantLeaderCheck**  
     A check that selects leaders  
   - **ParticipantResponsibleCheck**  
     A check that selects camp responsibles  
   - **ParticipantAdultCheck**  
     A check that selects 21-year-olds  
   - **FileUploadCheck**  
     A check that contains a file  
   - **CommentCheck**  
     A check that contains comments  
   - **NumberCheck**  
     A check that contains numbers  

## **FIXTURES**  

  1. **CAMP TYPES:**  
     - FIXTURE: `src/apps/camps/fixtures/camp_types.json`  
     - COMMAND: `django-manage.py runfixtures`  
     - Defines the camp types that can be selected in the frontend and are linked in the categories and sub-categories.  
  2. **SCOUTS GROUP TYPES:**  
      - FIXTURE: `src/apps/groups/fixtures/scouts_group_types.json`  
      - COMMAND: `django-manage.py runfixtures`  
      - Defines the different group types (as per GroepAdmin). A parent group type can be defined to further classify a group type.  
  3. **DEFAULT SCOUTS SECTIONS:**  
      - FIXTURE: `src/apps/groups/fixtures/default_scouts_section_names.json`  
      - COMMAND: `django-manage.py runfixtures`  
      - Links the group type with the section name to determine the list of default scouts sections a group has.  
  4. **CATEGORY SET PRIORITIES:**  
      - FIXTURE: `src/apps/visums/fixtures/category_priorities.json`  
      - COMMAND: `django-manage.py runfixtures`  
      - Determines the precedence of one category set over another. Currently not in use anymore.  
  5. **CHECK TYPES:**  
      - FIXTURE: `src/apps/visums/fixtures/check_types.json`  
      - COMMAND: `django-manage.py runfixtures`  
      - Specifies the different types of checks. DO NOT CHANGE. Changes to this file require change in both back- and front-end. Contact inuits.  

## **COMMANDS**  

1. **`runfixtures`**  
   Uses django's loaddata command to load the following fixtures (in order):  
   - groups/fixtures/scouts_group_types.json
   - groups/fixtures/default_scouts_section_names.json
   - camps/fixtures/camp_types.json
   - visums/fixtures/category_priorities.json
   - visums/fixtures/check_types.json
