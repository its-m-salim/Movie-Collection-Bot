from html import escape


def movie_caption(movie, show_description=False):
    title = escape(str(movie['title']))
    genre = escape(str(movie['genre']))
    owner = escape(str(movie['full_name'] or 'Неизвестный пользователь'))

    lines = [
        f"🎬 <b>{title}</b>",
        "",
        f"📅 <b>Год выхода:</b> {movie['release_year']}",
        f"🎭 <b>Жанр:</b> {genre}",
        f"👤 <b>Добавил:</b> {owner}",
        f"❤️ В избранном: {movie['fav_count']}"
    ]

    if show_description:
        description = movie['caption']

        lines.extend([
            "",
            "📝 <b>Описание:</b>",
            escape(str(description)) if description else "Описание пока не добавлено."
        ])

    return "\n".join(lines)