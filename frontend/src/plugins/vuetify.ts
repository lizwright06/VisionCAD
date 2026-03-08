//imports
import type { App } from "vue";
import { createVuetify } from "vuetify";
import { aliases, mdi } from "vuetify/iconsets/mdi";
import type { ThemeDefinition } from "vuetify";
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css'

export default (app: App) => {
    //themes
    const themes: Record<string, ThemeDefinition> = {
        light: {
            dark: false,
            colors: {
                //TODO: clean up palette & take out comments
                primary: '#A05DCB',
                'primary-darken': '#57058B',

                secondary: '#8A2FC9',
                'secondary-darken': '#6F0E96',

                'on-primary': '#FFFFFF',
                'on-secondary': '#FFFFFF',
                background: '#EAD9F9',
                surface: '#D0B4EF',
            },
            variables: {

            }
        }
    };

    //defaults
    const defaults = {
        VBtn: {
            color: "secondary",
            rounded: "lg",
            style: "text-transform: none; font-weight: 500;",
            variant: "flat"
        },
        VCard: {
            color: "primary",
            flat: true,
            rounded: "lg",
            border: false,
        },
        VAppBar: {
            color: "primary-darken",
            VBtn: {
                color: "secondary",
                rounded: "lg",
                style: "text-transform: none; font-weight: 500;",
                variant: "flat"
            }
        },
        VFooter: {
            color: "primary-darken",
            VBtn: {
                color: "secondary",
                rounded: "lg",
                style: "text-transform: none; font-weight: 500;",
                variant: "flat"
            }
        },
        VFileUpload: {
            color: "primary"
        }
    };

    //creation
    const vuetify = createVuetify({
        aliases,
        defaults,
        theme: {
            defaultTheme: 'light',
            themes,
        },
        icons: {
            defaultSet: "mdi",
            aliases,
            sets: {
                mdi,
            },
        },
    });

    app.use(vuetify);
}