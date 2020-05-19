{{ objname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :no-members:
   :no-undoc-members:
   :show-inheritance:

   {% block methods %}

{% if methods %}
.. rubric:: Methods

.. autosummary::
    :template: autoFunction.rst
    :toctree: methods/{{ objname }}

    {% for item in methods %}
    {%- if item not in inherited_members %}
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
