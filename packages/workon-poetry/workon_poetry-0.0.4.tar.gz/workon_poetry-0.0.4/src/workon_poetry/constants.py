# constants.py
from pathlib import Path
import logging

from dotenv import load_dotenv, dotenv_values

DATA_DIR = Path(__file__).parent / 'data'

load_dotenv()
ENV = dotenv_values()
globals().update(vars(ENV))


try:
    import sentry_sdk
    SENTRY_PUBLIC_KEY = ENV.get('SENTRY_PUBLIC_KEY')

    # # All of the commented lines are happening by default! Uncomment and modify for custom behavior.

    # from sentry_sdk.integrations.logging import LoggingIntegration

    # sentry_logging = LoggingIntegration(
    #    level=logging.INFO,        # Capture info and above as breadcrumbs
    #    event_level=logging.ERROR  # Send errors as events
    # )
    sentry_sdk.init(
        dsn=f"https://{SENTRY_PUBLIC_KEY}@o0.ingest.sentry.io/0",
        # integrations=[
        #     sentry_logging,
        # ],

        # Set traces_sample_rate to 1.0 to capture 100% of all messages.
        # Reduce this to .05 or less on production.
        traces_sample_rate=1.0,
    )
except Exception as exc:
    logging.warn('Unable to import and configure sentry_sdk so using default Python logger')
    logging.error(str(exc))