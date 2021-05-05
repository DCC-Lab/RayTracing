{{ objname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :no-undoc-members:
   :show-inheritance:
   :inherited-members:

   {% block methods %}

{% if methods %}
.. rubric:: Methods

.. autosummary:: methods/{{ objname }}
    :template: autoFunction.rst

    {% for item in methods %}
    {%- if item not in inherited_members %}
        ~{{ name }}.{{ item }}
    {%- endif %}
    {%- endfor %}

.. rubric:: Inherited Methods

.. autosummary:: methods/{{ objname }}
    :template: autoInheritedFunction.rst

    {% for item in methods %}
    {%- if item in inherited_members %}
        ~{{ name }}.{{ item }}
    {%- endif %}
    {%- endfor %}

{% endif %}
{% endblock %}

{% block attributes %}
{% if attributes %}
.. rubric:: Attributes

.. autosummary::

    {% for item in attributes %}
      ~{{ name }}.{{ item }}
    {%- endfor %}
{% endif %}
{% endblock %}
