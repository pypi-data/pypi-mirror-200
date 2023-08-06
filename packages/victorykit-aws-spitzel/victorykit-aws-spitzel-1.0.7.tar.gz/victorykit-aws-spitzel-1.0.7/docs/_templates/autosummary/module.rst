{{ fullname | escape | underline }}

.. rubric:: Description

.. automodule:: {{ fullname }}
    :special-members:

.. currentmodule:: {{ fullname }}

{% if modules %}
.. rubric:: Modules

.. autosummary::
    :toctree: .
    :recursive:
    {% for module in modules %}
    {{ module }}
    {% endfor %}

{% endif %}

{% if classes %}
.. rubric:: Classes

.. autosummary::
    :toctree: .
    {% for class in classes %}
    {{ class }}
    {% endfor %}

{% endif %}

{% if functions %}
.. rubric:: Functions

.. autosummary::
    :toctree: .
    {% for function in functions %}
    {{ function }}
    {% endfor %}

{% endif %}