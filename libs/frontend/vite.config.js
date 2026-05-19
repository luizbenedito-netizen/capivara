import {defineConfig, searchForWorkspaceRoot} from 'vite';
import {djangoVitePlugin} from 'django-vite-plugin';
import path from 'path';

const isDev = process.env.NODE_ENV !== 'production';

export default defineConfig({
    appType: 'custom',
    root: '.',
    server: {
        port: 5173,
        cors: true,
        fs: {
            allow: [
                searchForWorkspaceRoot(process.cwd()),
                path.resolve(__dirname, '../../static'),
            ],
        },
    },
    base: isDev ? '/' : '/static/',
    resolve: {
        alias: {
            '@static': path.resolve(__dirname, '../../static'),
        },
    },
    build: {
        outDir: path.resolve(__dirname, '../../static'),
        emptyOutDir: false,
    },
    plugins: [
        {
            name: 'remove-django-static-prefix',
            configureServer(server) {
                server.middlewares.use((req, res, next) => {
                    if (req.url && req.url.startsWith('/static/')) {
                        req.url = req.url.replace('/static/', '/');
                    }
                    next();
                });
            },
        },
        djangoVitePlugin({
            root: path.resolve(__dirname, '../..'),
            pyPath: path.resolve(__dirname, '../../venv/bin/python'),
            inputBase: 'frontend',
            input: [
                './layout/templates/home.js',
                './layout/pages/heart/heart.js',
                './layout/pages/dashboard/dashboard.js',
                './layout/pages/user/user.js',
                './layout/pages/user/settings.js',
            ],

        }),

    ],

});