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
                background: '#ffffff',
                surface: '#7d0f30',
                "on-surface": '#ffffff',
                primary: '#eb4d89',
                "on-primary": '#ffffff',
                secondary: '#e71655',
                "on-secondary": '#ffffff'
                //error
                //info
                //success
                //warning
            },
            variables: {

            }
        },
        // dark: {
        //     dark: true,
        //     colors: {
        //         background: '#ffffff',
        //         surface: '#7d0f30',
        //         "on-surface": '#ffffff',
        //         primary: '#eb4d89',
        //         "on-primary": '#ffffff',
        //         secondary: '#e71655',
        //         "on-secondary": '#ffffff'
        //         //error
        //         //info
        //         //success
        //         //warning
        //     },
        //     variables: {
                
        //     }
        // }
    };

    //defaults
    const defaults = {
        VBtn: {
            color: "secondary",
            rounded: "lg",
            style: "text-transform: none; font-weight: 500;",
        },
        VCard: {
            flat: true,
            rounded: "lg",
            border: false,
        },
        VAppBar: {
            color: "primary",
            VBtn: {
                color: "secondary",
                rounded: "lg",
                style: "text-transform: none; font-weight: 500;",
                variant: "flat"
            }
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