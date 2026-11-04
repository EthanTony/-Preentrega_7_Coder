import os
import shutil
import tempfile

from django.contrib.auth.models import AnonymousUser, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Post


class PostModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="autor", password="ClaveSegura123!")
        cls.other_user = User.objects.create_user(username="otro", password="ClaveSegura123!")
        cls.staff_user = User.objects.create_user(
            username="staff", password="ClaveSegura123!", is_staff=True
        )
        cls.post = Post.objects.create(
            title="Primera publicación",
            content="Contenido de prueba",
            author=cls.author,
        )

    def test_str_returns_title(self):
        self.assertEqual(str(self.post), "Primera publicación")

    def test_get_absolute_url_uses_detail_route(self):
        self.assertEqual(
            self.post.get_absolute_url(),
            reverse("posts:post_detail", kwargs={"pk": self.post.pk}),
        )

    def test_post_without_image_is_allowed(self):
        self.assertFalse(bool(self.post.image))

    def test_author_can_edit(self):
        self.assertTrue(self.post.can_be_edited_by(self.author))

    def test_staff_can_edit(self):
        self.assertTrue(self.post.can_be_edited_by(self.staff_user))

    def test_other_user_cannot_edit(self):
        self.assertFalse(self.post.can_be_edited_by(self.other_user))

    def test_anonymous_cannot_edit(self):
        self.assertFalse(self.post.can_be_edited_by(AnonymousUser()))

    def test_posts_are_ordered_newest_first(self):
        newer = Post.objects.create(
            title="Más reciente",
            content="Otra publicación",
            author=self.author,
        )
        self.assertEqual(Post.objects.first(), newer)


class PostViewTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="autor", password="ClaveSegura123!")
        self.other_user = User.objects.create_user(username="otro", password="ClaveSegura123!")
        self.staff_user = User.objects.create_user(
            username="staff", password="ClaveSegura123!", is_staff=True
        )
        self.post = Post.objects.create(
            title="Django para principiantes",
            content="Una guía introductoria sobre Django y sus vistas.",
            author=self.author,
        )

    def test_list_view_is_public(self):
        response = self.client.get(reverse("posts:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.author.username)

    def test_detail_view_is_public(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)

    def test_search_by_title(self):
        other = Post.objects.create(
            title="Python avanzado",
            content="Contenido diferente.",
            author=self.author,
        )
        response = self.client.get(reverse("posts:post_list"), {"q": "django"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertNotContains(response, other.title)
        self.assertEqual(response.context["query"], "django")

    def test_search_by_content(self):
        response = self.client.get(reverse("posts:post_list"), {"q": "introductoria"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_search_without_results_shows_message(self):
        response = self.client.get(reverse("posts:post_list"), {"q": "inexistente"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No se encontraron publicaciones")
        self.assertContains(response, "inexistente")

    def test_list_renders_post_without_image(self):
        response = self.client.get(reverse("posts:post_list"))
        self.assertContains(response, "Sin imagen")

    def test_anonymous_cannot_create(self):
        response = self.client.get(reverse("posts:post_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
        self.assertIn("next=", response.url)

    def test_create_form_renders_for_authenticated_user(self):
        self.client.login(username="autor", password="ClaveSegura123!")
        response = self.client.get(reverse("posts:post_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nueva publicación")
        self.assertContains(response, 'enctype="multipart/form-data"')

    def test_edit_form_renders_for_author(self):
        self.client.login(username="autor", password="ClaveSegura123!")
        response = self.client.get(
            reverse("posts:post_update", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Editar publicación")

    def test_authenticated_user_can_create(self):
        self.client.login(username="autor", password="ClaveSegura123!")
        response = self.client.post(
            reverse("posts:post_create"),
            {"title": "Nueva publicación", "content": "Contenido nuevo"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        created = Post.objects.get(title="Nueva publicación")
        self.assertEqual(created.author, self.author)
        self.assertRedirects(response, created.get_absolute_url())
        self.assertContains(response, "La publicación se creó correctamente.")

    def test_author_can_edit(self):
        self.client.login(username="autor", password="ClaveSegura123!")
        response = self.client.post(
            reverse("posts:post_update", kwargs={"pk": self.post.pk}),
            {"title": "Título actualizado", "content": self.post.content},
            follow=True,
        )
        self.assertRedirects(response, self.post.get_absolute_url())
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Título actualizado")

    def test_anonymous_cannot_edit(self):
        response = self.client.get(
            reverse("posts:post_update", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_non_author_cannot_edit(self):
        self.client.login(username="otro", password="ClaveSegura123!")
        response = self.client.post(
            reverse("posts:post_update", kwargs={"pk": self.post.pk}),
            {"title": "Intento no autorizado", "content": "Contenido"},
        )
        self.assertEqual(response.status_code, 403)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Django para principiantes")

    def test_staff_can_edit_other_user_post(self):
        self.client.login(username="staff", password="ClaveSegura123!")
        response = self.client.post(
            reverse("posts:post_update", kwargs={"pk": self.post.pk}),
            {"title": "Editado por staff", "content": self.post.content},
            follow=True,
        )
        self.assertRedirects(response, self.post.get_absolute_url())
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Editado por staff")

    def test_author_can_delete(self):
        self.client.login(username="autor", password="ClaveSegura123!")
        response = self.client.get(
            reverse("posts:post_delete", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "¿Seguro que quieres eliminar")

        response = self.client.post(
            reverse("posts:post_delete", kwargs={"pk": self.post.pk}),
            follow=True,
        )
        self.assertRedirects(response, reverse("posts:post_list"))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
        self.assertContains(response, "La publicación se eliminó correctamente.")

    def test_non_author_cannot_delete(self):
        self.client.login(username="otro", password="ClaveSegura123!")
        response = self.client.post(
            reverse("posts:post_delete", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_staff_can_delete_other_user_post(self):
        self.client.login(username="staff", password="ClaveSegura123!")
        response = self.client.post(
            reverse("posts:post_delete", kwargs={"pk": self.post.pk})
        )
        self.assertRedirects(response, reverse("posts:post_list"))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario", password="ClaveSegura123!"
        )

    def test_register_view_is_public(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Crear cuenta")

    def test_register_creates_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "nuevo_usuario",
                "email": "nuevo@example.com",
                "password1": "ClaveMuySegura2026!",
                "password2": "ClaveMuySegura2026!",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="nuevo_usuario").exists())
        self.assertContains(response, "Tu cuenta se creó correctamente")

    def test_register_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "nuevo_usuario",
                "password1": "ClaveMuySegura2026!",
                "password2": "OtraClaveDistinta2026!",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="nuevo_usuario").exists())

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {"username": "usuario", "password": "ClaveSegura123!"},
            follow=True,
        )
        self.assertRedirects(response, reverse("posts:post_list"))
        self.assertIn("_auth_user_id", self.client.session)
        self.assertContains(response, "Bienvenido, usuario.")

    def test_logout_via_post(self):
        self.client.login(username="usuario", password="ClaveSegura123!")
        response = self.client.post(reverse("logout"), follow=True)
        self.assertRedirects(response, reverse("posts:post_list"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertContains(response, "Has cerrado sesión correctamente.")

    def test_logout_get_is_not_allowed(self):
        self.client.login(username="usuario", password="ClaveSegura123!")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 405)

    def test_navigation_differs_for_anonymous_and_authenticated(self):
        response = self.client.get(reverse("posts:post_list"))
        self.assertContains(response, "Iniciar sesión")
        self.assertContains(response, "Registrarse")
        self.assertNotContains(response, "Cerrar sesión")

        self.client.login(username="usuario", password="ClaveSegura123!")
        response = self.client.get(reverse("posts:post_list"))
        self.assertContains(response, "Nueva publicación")
        self.assertContains(response, "Cerrar sesión")
        self.assertNotContains(response, "Registrarse")


class PostImageTests(TestCase):
    # GIF transparente de 1x1 píxel para validar ImageField sin depender de archivos externos.
    TINY_GIF = (
        b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04"
        b"\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D"
        b"\x01\x00;"
    )

    @classmethod
    def setUpClass(cls):
        cls._media_dir = tempfile.mkdtemp()
        cls._override = override_settings(MEDIA_ROOT=cls._media_dir)
        cls._override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls._override.disable()
        shutil.rmtree(cls._media_dir, ignore_errors=True)

    def setUp(self):
        self.user = User.objects.create_user(
            username="con_imagen", password="ClaveSegura123!"
        )
        self.client.login(username="con_imagen", password="ClaveSegura123!")

    def test_create_post_with_image(self):
        upload = SimpleUploadedFile(
            "imagen.gif", self.TINY_GIF, content_type="image/gif"
        )
        response = self.client.post(
            reverse("posts:post_create"),
            {"title": "Con imagen", "content": "Publicación con imagen.", "image": upload},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        post = Post.objects.get(title="Con imagen")
        self.assertTrue(post.image)
        self.assertTrue(os.path.exists(post.image.path))
        self.assertContains(response, post.image.url)

    def test_create_post_without_image(self):
        response = self.client.post(
            reverse("posts:post_create"),
            {"title": "Sin imagen", "content": "Publicación sin imagen."},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        post = Post.objects.get(title="Sin imagen")
        self.assertFalse(bool(post.image))
        self.assertContains(response, "Sin imagen")
