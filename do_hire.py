def make_hire():
    strok = """{% extends "base.html" %}

{% block content %}
<h1 style="height:100px; width:1024px; background:#e6a8d7">Афиша</h1>
<form action="" method="post">
    <div class="new-list list-place" data-test="list">
        <div class="new-list__item new-list-place__item" data-test="ITEM">
"""

    fil = [i.split('|') for i in open('hire.txt', encoding="utf-8").read().split('\n')]
    for i in range(len(fil)):
        strok += """
            <div class="new-list__item-info" style="height:100px; width:1024px; background:#ccccff">
                <h3>
                    <a href=""" + """""""" + str(
            i) + """""""" + """ class="new-list__item-link" data-test="ITEM-URL">""" + fil[i][0] + """</a>"""

        strok += """\n                  <p><img src=""" + f'"../photos/{fil[i][1]}" alt="{fil[i][0]}"' + """/></p>"""
        strok += """\n                </h3>
                    </div>"""

    strok += """
        </div>
    </div>
</form>
{% endblock %}"""

    return strok


def load_hire_to_html():
    f = open("templates/hire.html", 'w', encoding='utf-8')
    f.write(make_hire())
    f.close()
