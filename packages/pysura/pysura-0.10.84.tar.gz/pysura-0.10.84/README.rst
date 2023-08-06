
Pysura - BETA
=============

Hasura + Python = Pysura. An open source solution.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Requirements:
-------------

To deploy Hasura with Pysura with baked in Auth and a templated Flutter Frontend:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


* gcloud CLI
* gcloud beta CLI
* A billing account with Google Cloud
* Docker (Make sure it's running in the background or your deployment will fail!)
* Python 3.9+
* Firebase CLI
* npm
* flutterfire_cli
* Dart
* Flutter
* XCode (for iOS apps) and iOS Dev Tools
* Android Studio (for Android apps) and Android Dev Tools
* Gradle (for Android apps)

.. code-block:: commandline

   pip install pysura
   pysura
   (pysura_cli) >>> choose_provider
   Please choose a provider: [google,]: google
   (pysura_cli) >>> setup_pysura

Note: The installer is doing a lot of things. Some of them take a long time, like creating databases, firewalls, and VPC
networks. Sometimes it might look frozen, but give it some time to do its thing. It's automagically building an entire
application for you. I promise doing this by hand takes longer. ;)

Is this multi-platform compatible?
----------------------------------

Mac - Yes, I developed it on a Mac!

Linux - It should work on Linux, it is untested. Let me know!

Windows - I think so, but please let me know!

What is Pysura?
===============

Pysura is a CLI tool that's designed to make building and deploying multi-tenant enterprise grade applications as easy
as a freshman year algorithms class. It's a highly opinionated way because it's the right way.

It's kind of like running npm init, if npm was for backends and frontends, it provides your backend, auth, and database
for you in the cloud in a way that is infinitely scalable and uses zero-trust, with a type-safe GraphQL backend and a
bring-your-own front-end approach with special built-in support for Flutter which is the default setup.

Why Flutter?

So that it doesn't matter what you are building, you can build it on Pysura. It's about damn time that Python developers
have better mobile support. Let's bring python to mobile. Let's bring python to the web. Let's bring python to the edge.
Let's bring python everywhere. And let's skin it with Flutter and feed it all the data it wants with GraphQL and Hasura.

What is a Pysura Microservice?

It's a wrapper around a FastAPI app that holds a collection of actions, events, and chron-jobs related to it's function.
I.e. A payment microservice might have all code related to payment processing. It bakes in Auth with an extra decorator
which gives you easy access to the calling user each time a method is called. This works by using opaque tokens that
pass through the headers into the microservice. It's a very simple way to do auth, and it's very secure. It gives full
RBAC at a column level, and you can design rather complex auth rules using Hasura's permission system.

Do I need to deploy Hasura with Pysura to use it?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As of right now yes. In the future, no!

Is this just a wrapper for the Hasura CLI?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pysura does *not* use the Hasura CLI, and instead manages the metadata directly via retrieving it and overwriting it.

It's important to note that Pysura will add the local machine of its installer's IP to the allow-list for the database.
This is to allow pysura to connect via pscopg2 for things like table management. You'll need to de-authorize the network
if you want to remove the machine from the allow-list once setup is complete. TODO: Make a deauthorize command.

Limitations:
^^^^^^^^^^^^

Currently, this only supports a Google-based deployment/stack. Easily fixable. Just need a fellow AWS/Azure/Etc. wizard
who can translate the gcloud commands. I think the portability is pretty high since everything is done from the CLI. The
setup wizard is just curling everything.

Neat! But it doesn't support my cloud provider, when will you be adding AWS/Azure/Etc. support?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I won't. You can. I built this because I needed it. If our stack changes providers, or potentially if someone was
willing to pay for it, I'd be willing to add support for other providers. But as of now, the best bet would be to open a
PR and add support for your provider of choice. I tried to design it to be pretty modular. The gcloud --format=json flag
is what changed the game when I found it. Maybe try ChatGPT to translate the gcloud commands to AWS/Azure/Etc. commands.

FAQ:
^^^^

Q: I broke the installer, something wasn't enabled properly. (I didn't have docker running, didn't have gcloud
installed, etc.)

A: Best bet is to try to rerun the installer, it might throw some errors but it should recover for the most part. If it
doesn't, then you should trash the project and rerun the setup. Just remember to go to billing and disable the old
project, and shut it down.

Q: How do I contribute?

A: Read over the current code, and see if you can make it better. If you can, open a PR. If you can't, open an issue or
a feature request for something that would make it better.

Q: Is this affiliated with Hasura, Google, or Firebase?

A: No, this has no affiliation with Hasura, Google, or Firebase. In no way should this be considered an official product
of any of these companies. Although this makes heavy use of tools and API's provided it is in no way an official product
of any company or tool used.

TODOS:
^^^^^^

DONE:


* [x] Add support for Google Cloud
* [x] Add support for Firebase Auth
* [x] Add ios/android wizard
* [x] Add support for Flutter
* [x] Hasura Autodeployer

HIGH PRIORITY:


* [ ] Add table manager @Tristen
* [ ] Add microservice manager @Tristen
* [ ] Add action wizard @Tristen
* [ ] Add event wizard @Tristen
* [ ] Add cron wizard @Tristen
* [ ] Add support for other auth providers (Auth0, etc) @Unclaimed

  * [ ] Auth0
  * [ ] ???

* [ ] Flutter SSR bindings for Web @Unclaimed
* [ ] Caching Wizard @Tristen
* [ ] Update the pysura/pysura_types/root_cmd.py to make better use of prompt_toolkit. It would be nice to have multiple
  tabs for different level of logs. @Unclaimed
* [ ] Built in API Version Control @Tristen
* [ ] Tighten up the command loops. (Ex. Test the deployer and input values that will fail, and make sure it can recover
  more gracefully) @Unclaimed

LOW PRIORITY:


* [ ] Add support for AWS/Azure/Etc.
* [ ] Add support for other databases (Postgres, MySQL, BigQuery, etc)
* [ ] Add support for other frontends (React, Vue, etc)
