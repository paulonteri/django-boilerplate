# StyleGuide

This is the main guide: [https://github.com/HackSoftware/Django-Styleguide](https://github.com/HackSoftware/Django-Styleguide)

We can also take some inspiration from

- [https://github.com/phalt/django-api-domains](https://github.com/phalt/django-api-domains)
- <https://sensidev.net/blog/django-service-layer>
- <https://ui.dev/imperative-vs-declarative-programming/>

## Domain

A [domain](<https://en.wikipedia.org/wiki/Domain_(software_engineering)>) is a piece of software that provides a distinct **business** value for your application.

What this styleguide calls a `domain` is roughly an extension of what Django would call an `app`. Therefore a business domain **should** have at least one distinct software domain mirroring it.

A domain **should** use the following file structure:

```
- apis.py - Public functions and access points, presentation logic.
- models.py - Object models and storage, simple information logic.
- services.py - Business logic, handling complexity, coordination and transactional logic
- tasks.py - Asynchronous tasks, e.g. email sending, etc.
- jobs.py - Scheduled jobs, etc. Often used to call tasks.
- interfaces.py - Integrations with other domains or external services.
```

**Which logic lives where?**

It's common in programming to end up confused about what type of logic should live where.

There are many cases where it's difficult to decide, and the best advice is to **pick a pattern and stick to it**, but for simpler things, this guide emphasises the following:

---

### Models

Logic around information.

> **If you ask:**
> "Where can I store this data?" or "Where can I do any post/pre-save actions?"

- Models **must not** have any complex functional logic in them.
- Models **should** own informational logic related to them.
- Models **can** have computed properties where it makes sense.
- Models **must not** import services, interfaces, or apis from their own domain or other domains.

---

### Services

Often used to taken our [imperative](https://youtu.be/E7Fbf7R3x6I)  (& operational - the many steps taken to reach a goal/solution/complete task) light code (mostly business logic) and abstract it behind a [declarative](https://ui.dev/imperative-vs-declarative-programming) api.

Simple example comparing declarative vs imperative:

> **Imperative response**: Go out of the north exit of the parking lot and take a left. Get on I-15 North until you get to the 12th street exit. Take a right off the exit like you’re going to Ikea. Go straight and take a right at the first light. Continue through the next light then take your next left. My house is #298.

> **A declarative response**: My address is 298 West Immutable Alley, Eden, Utah 84310

If the steps taken in first example are useful, they should probably live in services.py instead of being copy-pasted everywhere.

Services have a lot of logic around coordination and transactions.  Majority of the business logic should live here.

> **If you ask:**
> "Where do I coordinate updating many models in one domain?" or "Where do I dispatch a single action out to other domains?"

Everything in a domain comes together in Services.

_Services_ gather all the business value for this domain. What type of logic should live here? Here are a few examples:

- When creating a new instance of a model, we need to compute a field on it before saving.
- When querying some content, we need to collect it from a few different places and gather it together in a python object.
- When deleting an instance we need to send a signal to another domain so it can do it's own logic.

Anything that is specific to the domain problem and **not** basic informational logic should live in Services. As most API projects expose single functional actions such as Create, Read, Update, and Delete, _Services_ has been designed specifically to compliment stateless, single-action functions.

- Services **should** own co-ordination and transactional logic.
- Functions in services.py **must** use type annotations.
- Functions in services.py **must** use keyword arguments.
- You **should** be logging in `services.py`.

---

### APIs

Logic about presentation.

> **If you ask:**
> "Where should I show this data to the user?" or "Where do I define the API schema?"

APIs defines the external API interface for your domain. Anyone using the APIs defined here is called a consumer.

- Internal functions in APIs **must** use type annotations.
- Internal functions in APIs **must** use keyword arguments.
- You **should** log API function calls.
- All data returned from APIs **must be** serializable.
- APIs **should** talk to **Services** to get data.
- APIs **should** do simple logic like transforming data for the outside world, or taking external data and transforming it for the domain to understand.
- Objects represented through APIs **do not** have to map directly to internal database representations of data.

Examples:

```python
class ExamsAPI(viewsets.ModelViewSet):
    permission_classes = [DEFAULT_PERMISSIONS]
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()

    @action(detail=True, methods=['get'])
    def analyse_results(self, request, pk):
        """
        Does exam analysis and ranking
        """
        results = ExamsService.analyse_results(exam_pk=pk)
        serializer = ExamResultsAnalysisCacheSerializer(results)

        return Response(serializer.data)
```

```python
class SendExamResultsAPI(generics.CreateAPIView):

    class InputSerializer(serializers.Serializer):
        time_to_send = serializers.DateTimeField(default=timezone.now)
        send_to_students_too = serializers.BooleanField(default=False)

    queryset = ExamStudentSubjectResult.objects.all()
    serializer_class = InputSerializer
    permission_classes = [DEFAULT_PERMISSIONS]

    def post(self, request, exam_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        exam_release = ExamsService.get_or_create_release(
            exam=get_object_or_404(Exam, pk=exam_id)
        )

        ExamReleasesService.send_results_sms(
            exam_release_pk=exam_release.pk,
            time_to_send=serializer.data["time_to_send"],
            send_to_students_too=serializer.data["send_to_students_too"]
        )

        return Response(status=status.HTTP_201_CREATED)
```

---

### Tasks

> **If you ask:**
> "How do I run this outside of the request context?"

Async tasks executed by Google Cloud Tasks.

Ensure that the task is idempotent and completes in less than 60 seconds (Aim for around 30). The time limit is because of a CloudFlare [limitation](https://support.cloudflare.com/hc/en-us/articles/115003011431-Troubleshooting-Cloudflare-5XX-errors#524error).

Example task:

```python
from .services import ExamReleaseSmsService

def send_sms_results():
    ExamReleaseSmsService.send_messages_in_queue()
```

---

### Jobs

 Scheduled jobs/functions executed at a regular interval. Need to be added to `settings.py`.

Often call tasks from `tasks.py`.

> **If you ask:**
> "I want to run this job every day at midnight, but I don't know how to do that." or
> "Where do I place the function that will that does x every n time?"

Ensure that the task is idempotent and completes in less than 60 seconds (Aim for around 30). The time limit is because of a CloudFlare [limitation](https://support.cloudflare.com/hc/en-us/articles/115003011431-Troubleshooting-Cloudflare-5XX-errors#524error).

Example job:

```python

from shulesuite.apps_public.async_tasks.services import AsyncTasksServices
from shulesuite.apps_public.schools.decorators import run_in_all_schools
from shulesuite.apps_school.examinations.models import ExamReleaseSmsMessage
from .tasks import send_sms_results


@run_in_all_schools
def check_if_there_are_sms_results_to_send_and_send_them():

    if ExamReleaseSmsMessage.objects.filter(sent_at__isnull=True).exists():
        AsyncTasksServices.create_cloud_task(
            task=send_sms_results,
        )
```

---

### Interfaces

Logic for handling the transformation of data from other domains.

> **If you ask:**
> "Where shall I connect to another domain?" or "How do I change the data format for another domain?"

Your domain may need to communicate with another domain. That domain can be in another web server across the web, or it could be within the same server. It could even be a third-party service. When your domain needs to talk to other domains, you should define **all interactions to the other domain in the `interfaces.py` file**. Combined with APIs (see above), this forms the bounded context of the domain and prevents domain logic from leaking in.

Consider `interfaces.py` like a mini _Anti-Corruption Layer_. Most of the time it won't change and it'll just pass on arguments to an API function. But when the other domain moves - say you extract it into its own web service, your domain only needs to update the code in `interfaces.py` to reflect the change. No complex refactoring needed, woohoo!

It's worth noting that some guides would consider this implementation a 'code smell' because it has the potential for creating shallow methods or pass-through methods. If you find your `interfaces.py` is redundant, then you probably don't need it. That said: **we recommend starting with it and removing it later**.

- Functions in Interfaces **must** use type annotations.
- Functions in Interfaces **must** use keyword arguments.
