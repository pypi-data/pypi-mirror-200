from django.urls import reverse

from wagtail.test.utils.form_data import (
    nested_form_data,
    rich_text,
    streamfield,
)

import pytest
from pytest_django.asserts import assertContains

from .models import StandardPage


@pytest.mark.django_db
def test_insert_editor_css(admin_client, root_page):
    response = admin_client.get('/admin/pages/%d/edit/' % root_page.id)
    assertContains(response, 'wagtail_cblocks/css/editor.css')


@pytest.mark.django_db
class TestStylizedStructBlock:
    def test_page_preview(self, admin_client, root_page):
        add_url = reverse(
            'wagtailadmin_pages:add',
            args=('tests', 'standardpage', root_page.id),
        )

        form_data = nested_form_data(
            {
                'title': "A page",
                'body': streamfield(
                    [
                        (
                            'hero_block',
                            {
                                'style': 'centered',
                                'blocks': streamfield(
                                    [
                                        (
                                            'paragraph_block',
                                            rich_text('<p>Lorem ipsum</p>'),
                                        ),
                                    ]
                                ),
                            },
                        ),
                    ]
                ),
            }
        )
        form_data['slug'] = 'a-page'
        response = admin_client.post(add_url, data=form_data)
        assert response.status_code == 302

        page = StandardPage.objects.get(slug='a-page')
        preview_url = reverse('wagtailadmin_pages:view_draft', args=(page.id,))

        response = admin_client.get(preview_url)
        assert response.status_code == 200
        assertContains(response, 'hero-centered')
        assertContains(response, 'Lorem ipsum')
