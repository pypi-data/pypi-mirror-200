import copy

class Deployment:
    """
    Class containing functions to work with Deployment yaml files
    """

    def __init__(self, deployment):
        self.original_deployment = deployment
        self.deployment = copy.deepcopy(self.original_deployment)

        self.name = ''
        self.containers = []

        if 'metadata' in self.deployment and 'name' in self.deployment['metadata']:
            self.name = self.deployment['metadata']['name']

        if 'containers' in self.deployment['spec']['template']['spec']:
            self.containers = self.deployment['spec']['template']['spec']['containers']

    def set_image(self, new_image, container_name=None):
        for c in self.containers:
            if container_name:
                if c['name'] == container_name:
                    c['image'] = new_image
            else:
                c['image'] = new_image

    def get_updated(self):
        self.deployment['spec']['template']['spec']['containers'] = self.containers
        return self.deployment

    def get_containers(self):
        return self.containers
