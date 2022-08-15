# K8s

## Introduction

The application(s) is packaged using Helm <https://helm.sh/>

### Notes

- The default namespace is defined in the `values.yaml` under `nameSpace`.

---

## Setup

From the k8s folder:

### First time

<https://helm.sh/docs/intro/using_helm/#helm-install-installing-a-package>

```bash
helm install release-name k8s --atomic
```

### Updates

<https://helm.sh/docs/intro/using_helm/#helm-upgrade-and-helm-rollback-upgrading-a-release-and-recovering-on-failure>

```bash
helm upgrade release-name k8s --atomic
```

---

## Configuration

### Use an External Database

If you wan to use an external database, you can [override](https://helm.sh/docs/chart_template_guide/values_files/) the following values in the values.yaml file:

- Set `postgresql.enabled` to false.
- Set the `env.EXTERNAL_DB_HOST` to the host of the external database.
- Set the `env.DB_NAME`, `env.DB_USER` and `env.DB_PASSWORD` to the credentials of the external database.

### Disable Persistent Volume creation

Set `volumes.enabled` to false.

### Disable Load Balancer creation

Set `loadbalancers.enabled` to false.

---

## Other

### View

```bash
kubectl get pods -n dab
```

The above should have this kind of output:

```txt
NAME                            READY   STATUS      RESTARTS   AGE
celery-beat-667566f69f-9vlpm    1/1     Running     0          2m19s
celery-worker-9f77b8bb6-rm5qh   1/1     Running     0          2m19s
django-559f59bdfc-vjr6k         1/1     Running     0          2m25s
django-migrations-v8h5t         0/1     Completed   0          3m27s
flower-69b6fbc8f4-gp7gg         1/1     Running     0          2m13s
postgres-dc7b88579-tcwmg        1/1     Running     0          4m13s
redis-79468d5498-cv9xn          1/1     Running     0          4m7s
```

```bash
kubectl get services -n dab
```

The above should have this kind of output:

```txt
NAME               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
django-service     ClusterIP   10.104.86.120    <none>        8000/TCP   2m31s
flower-service     ClusterIP   10.109.57.161    <none>        5555/TCP   2m18s
postgres-service   ClusterIP   10.105.197.211   <none>        5432/TCP   4m19s
redis-service      ClusterIP   10.105.89.228    <none>        6379/TCP   4m13s
```
