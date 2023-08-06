import os
import glob
import importlib
import inspect

from playwright.sync_api import sync_playwright

from watchtower_browser_testing.tracking_validation import EventQueue, RequestValidator
from watchtower_browser_testing import exceptions
from watchtower_browser_testing import config


class TestResult(object):

    def __init__(self,
                 test_name,
                 browser,
                 scenario=None,
                 event=None,
                 ok=True,
                 errors=None,
                 data=None):

        self.test_name = test_name
        self.scenario = scenario
        self.event = event
        self.browser = browser
        self.ok = ok
        self.errors = errors
        self.data = data


class TrackingTest(object):

    browsers = config.DEFAULT_BROWSERS

    pipeline_pattern = config.DEFAULT_PIPELINE_PATTERN

    def setUpInstance(self,
                      playwright,
                      browser,
                      headless=False):

        self.app = getattr(playwright, browser)
        self.browser = self.app.launch(headless=headless)
        self.context = self.browser.new_context()
        self.harvest_user_ids = []

    def tearDownInstance(self):

        self.context.close()
        self.browser.close()

    def beforeEach(self):

        self.page = self.context.new_page()

    def afterEach(self):

        self.page.close()

    def record_events(self):

        self.event_queue = EventQueue(url_pattern=self.pipeline_pattern)
        self.page.on('request', self.event_queue.register)

    def run(self,
            browser=None,
            headless=False,
            report_data=None):

        if browser is None:
            browsers = self.browsers
        else:
            browsers = [browser]

        self.results = []
        report_data = report_data or {}

        for browser in browsers:

            with sync_playwright() as playwright:

                self.setUpInstance(playwright, browser, headless=headless)

                tests = [func for func in dir(self) if func.startswith(config.SCENARIO_METHOD_PREFIX)]

                for test in tests:

                    scenario = test[len(config.SCENARIO_METHOD_PREFIX):]

                    self.beforeEach()

                    getattr(self, test)()
                    validation_setup = getattr(self, config.VALIDATION_METHOD_PREFIX + scenario)()

                    for event, setup in validation_setup.items():

                        validator = RequestValidator(**setup)
                        validator.select(self.event_queue.requests)

                        if validator.is_valid():
                            self.result(browser=browser, scenario=scenario, event=event, ok=True,
                                        data={'n_matched_requests': validator.n_matched_requests, **report_data})
                        else:
                            self.result(browser=browser, scenario=scenario, event=event, ok=False,
                                        errors=validator.errors,
                                        data={'n_matched_requests': validator.n_matched_requests, **report_data})

                    self.afterEach()

                self.tearDownInstance()

    def result(self,
               browser,
               scenario,
               event,
               ok,
               errors=None,
               data=None):

        self.results.append(
            TestResult(
                test_name=self.name,
                scenario=scenario,
                event=event,
                browser=browser,
                ok=ok,
                errors=errors,
                data=data)
        )

    @property
    def name(self):

        return self.__class__.__name__

    @property
    def description(self):

        return config.DEFAULT_TEST_DESCRIPTION



class TestRunner(object):

    def __init__(self,
                 modules=None,
                 directory=None):

        self.modules = modules
        self.directory = directory

    def run_tests(self,
                  headless=False,
                  browser=None):

        directory = self.directory or os.getcwd()

        mods = glob.glob(os.path.join(directory, "*.py"))
        test_files = [os.path.basename(f)[:-3] for f in mods
                      if os.path.isfile(f) and os.path.basename(f).startswith(config.TEST_FILE_PREFIX)]

        if self.modules:

            missing = set(self.modules) - set(test_files)
            if len(missing) > 0:
                raise exceptions.NotFoundError(f'Did not find test module(s): {", ".join(missing)}')

            test_files = [tf for tf in test_files if tf in self.modules]

        results = []

        for test_file in test_files:

            mod = importlib.import_module(test_file)

            tests = []
            for attr in dir(mod):
                if inspect.isclass(getattr(mod, attr)) and issubclass(getattr(mod, attr), TrackingTest):
                    if any(x.startswith(config.SCENARIO_METHOD_PREFIX) for x in dir(getattr(mod, attr))):
                        tests.append({'file': test_file, 'class': getattr(mod, attr)})

            for test in tests:

                test_instance = test['class']()
                report_data = {'file': test_file}
                test_instance.run(headless=headless,
                                  browser=browser,
                                  report_data=report_data)
                results.extend(test_instance.results)

        return results




