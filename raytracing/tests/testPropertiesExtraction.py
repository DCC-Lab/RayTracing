import envtest  # modifies path
from raytracing import *
from raytracing.ui.raytracing_app import *
import ast

inf = float("+inf")


class TestProperties(envtest.RaytracingTestCase):
    def testProperties(self):
        properties = "Lens(f=100,label='test',d=10)"

        # Wrap it in a fake function call so we can eval the keyword arguments
        expr = ast.parse(properties, mode="eval")
        print(ast.dump(expr))

        print(expr.body)
        # Extract the keyword arguments
        kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in expr.body.keywords}

        # print(kwargs)

    def testParser(self):
        class_name, kwargs = RaytracingApp.parse_element_call("Lens(f=100)")

        allowed_classes = {
            "Lens": Lens,  # Assuming Lens is defined somewhere
        }

        cls = allowed_classes.get(class_name)
        if cls is None:
            raise ValueError(f"Class {class_name} not allowed")

        instance = cls(**kwargs)
        print(instance)


if __name__ == "__main__":
    envtest.main()
